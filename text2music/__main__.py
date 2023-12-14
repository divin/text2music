import os

import gradio as gr  # type: ignore
import scipy  # type: ignore
import torch
from diffusers import MusicLDMPipeline

from .constants import DESCRIPTION


def get_fixed_file_name(file_name: str) -> str:
    """Fix the file name to avoid errors"""
    file_name = file_name.replace(" ", "_")
    file_name = file_name.replace(".wav", "")
    file_name = file_name.replace(".", "_")
    file_name = file_name.replace(",", "_")
    return file_name


def get_app() -> gr.Interface:
    def _generate_audio(
        prompt: str,
        negative_prompt: str,
        guidance_scale: float,
        num_waveforms_per_prompt: int,
        num_inference_steps: int,
        audio_length_in_s: int,
        file_name: str,
    ) -> str:
        """Generate music from text"""
        num_inference_steps = int(num_inference_steps)
        audio_length_in_s = int(audio_length_in_s)
        file_name = get_fixed_file_name(file_name=file_name)
        file_path = f"generated_audio/{file_name}.wav"
        data = text2music(
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            num_waveforms_per_prompt=num_waveforms_per_prompt,
            num_inference_steps=num_inference_steps,
            audio_length_in_s=int(audio_length_in_s),
        ).audios[0]
        scipy.io.wavfile.write(file_path, rate=16000, data=data)
        return file_path

    # Initialize the TTS
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    repo_id = "ucsd-reach/musicldm"
    text2music = MusicLDMPipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
    text2music = text2music.to(device)

    # Create the app
    with gr.Blocks(title="🎵 Text2Music") as app:
        gr.Markdown("# 🎵 Text2Music")

        with gr.Accordion("About", open=False):
            gr.Markdown(DESCRIPTION)

        # Text which will be converted to speech
        with gr.Group():
            prompt = gr.Textbox(label="Enter Prompt")

        # Advanced settings
        with gr.Accordion("Advanced Settings", open=False):
            negative_prompt = gr.Textbox(value=None, label="Negative Prompt")
            guidance_scale = gr.Slider(
                value=2.0, label="Guidance Scale", step=0.1, minimum=0.0, maximum=100.0
            )
            num_inference_steps = gr.Slider(
                value=25, label="Number of Inference Steps", step=1, minimum=1, maximum=1000
            )
            num_waveforms_per_prompt = gr.Slider(
                value=1, label="Number of Waveforms per Prompt", step=1, minimum=1, maximum=10
            )

        # Generate audio from prompt
        with gr.Row():
            with gr.Group():
                audio_length_in_s = gr.Slider(
                    value=10, label="Audio Length in Seconds", step=1, minimum=1, maximum=600
                )
                file_name = gr.Textbox(label="Enter a File Name")
                button = gr.Button("Generate Audio")

            with gr.Column():
                generated_audio_preview = gr.Audio(label="Generated Audio Preview")

        button.click(
            fn=_generate_audio,
            inputs=[
                prompt,
                negative_prompt,
                guidance_scale,
                num_waveforms_per_prompt,
                num_inference_steps,
                audio_length_in_s,
                file_name,
            ],
            outputs=[generated_audio_preview],
        )

    return app


if __name__ == "__main__":
    # Create folder for generated audio
    if not os.path.exists("generated_audio"):
        os.mkdir("generated_audio")

    # Launch the app
    app = get_app()
    app.launch(show_api=False)
