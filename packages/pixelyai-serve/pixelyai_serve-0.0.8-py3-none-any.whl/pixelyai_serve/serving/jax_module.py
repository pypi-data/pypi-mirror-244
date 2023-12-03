import jax.lax
from EasyDel import JAXServer, AutoEasyDelModelForCausalLM
from fjformer import get_float_dtype_by_name
from transformers import AutoTokenizer
import logging
from typing import List
from .utils import BaseClassAgent, DEFAULT_SYSTEM_PROMPT, prompt_model

logging.basicConfig(
    level=logging.INFO
)


class PixelyAIServeJax(JAXServer, BaseClassAgent):
    def __init__(self, config=None):
        super().__init__(config=config)
        self.gradio_app_custom = self.create_gradio_pixely_ai()

    @classmethod
    def load_from_torch(cls, repo_id, config=None):

        tokenizer = AutoTokenizer.from_pretrained(repo_id)
        model, param = AutoEasyDelModelForCausalLM.from_pretrained(
            repo_id=repo_id,
            dtype=get_float_dtype_by_name(config['dtype'] if config is not None else 'fp16'),
            param_dtype=get_float_dtype_by_name(config['dtype'] if config is not None else 'fp16'),
            precision=jax.lax.Precision('fastest'),
            device=jax.devices('cpu')[0]
            # _do_init=False
        )
        return cls.load_from_params(
            config_model=model.config,
            model=model,
            config=config,
            params=param,
            tokenizer=tokenizer,
            add_params_field=True,
            do_memory_log=False
        )

    @classmethod
    def load_from_jax(cls, repo_id, checkpoint_path, config_repo=None, config=None):
        # from huggingface_hub import hf_hub_download
        # path = hf_hub_download(repo_id, checkpoint_path)
        # tokenizer = AutoTokenizer.from_pretrained(repo_id)
        # config_model = LlamaConfig.from_pretrained(config_repo or repo_id)
        # model = FlaxLlamaForCausalLM(
        #     config=config_model,
        #     dtype=get_float_dtype_by_name(config['dtype'] if config is not None else 'fp16'),
        #     param_dtype=get_float_dtype_by_name(config['dtype'] if config is not None else 'fp16'),
        #     precision=jax.lax.Precision('fastest'),
        #     _do_init=False
        # )
        # return cls.load(
        #     path=path,
        #     config_model=config_model,
        #     model=model,
        #     config=config,
        #     tokenizer=tokenizer,
        #     add_params_field=True,
        #     do_memory_log=False
        # )
        raise NotImplemented('Not Implemented Err!')

    def process_gradio_custom(self, prompt, user_id, data, system, max_new_tokens, greedy):
        history = data.split('<|END_OF_MESSAGE|>') if data != '' else []
        system = system if system != '' else DEFAULT_SYSTEM_PROMPT
        his = []
        for hs in history:
            if hs != '':
                his.append(hs.split('<|END_OF_MESSAGE_TURN_HUMAN|>'))
        history = his
        string = self.prompt_model(
            message=prompt,
            chat_history=history or [],
            system_prompt=system
        )
        response = 'null'
        if not self.config.stream_tokens_for_gradio:

            for response, _ in self.process(
                    string=string,
                    greedy=greedy,
                    max_new_tokens=max_new_tokens,
            ):
                ...

        else:
            for response, _ in self.process(
                    string=string,
                    greedy=greedy,
                    max_new_tokens=max_new_tokens
            ):
                yield '', response
        return '', response

    def launch(self,
               share_chat: bool = False,
               share_inst: bool = False,
               share_custom: bool = True
               ):
        share_kwargs = {}
        assert not share_chat or not share_inst, 'you have to pass at least one of sharing options True'
        if share_chat:
            self.gradio_app_chat.launch(share=True)
            share_kwargs['chat'] = self.gradio_app_chat.share_url
        if share_inst:
            self.gradio_app_instruct.launch(share=True)
            share_kwargs['inst'] = self.gradio_app_instruct.share_url
        if share_custom:
            self.gradio_app_custom.launch(share=True)
            share_kwargs['custom'] = self.gradio_app_custom.share_url
        return share_kwargs

    @staticmethod
    def format_chat(history: List[List[str]], prompt: str, system: str = None) -> str:
        return prompt_model(message=prompt, system_prompt=system, chat_history=history)

    @staticmethod
    def prompt_model(message: str, chat_history, system_prompt: str):
        return prompt_model(message=message, chat_history=chat_history, system_prompt=system_prompt)
