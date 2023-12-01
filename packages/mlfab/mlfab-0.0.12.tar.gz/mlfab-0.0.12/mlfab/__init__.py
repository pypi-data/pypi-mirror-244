"""Defines the top-level mlfab API.

This package is structured so that all the important stuff can be accessed
without having to dig around through the internals. This is done by lazily
importing the module by name.

This file can be maintained by running the update script:

.. code-block:: bash

    python -m scripts.update_api --inplace
"""

__version__ = "0.0.12"

# This list shouldn't be modified by hand; instead, run the update script.
__all__ = [
    "UserConfig",
    "field",
    "get_data_dir",
    "get_pretrained_models_dir",
    "get_run_dir",
    "get_stage_dir",
    "load_user_config",
    "State",
    "cast_phase",
    "Clamp",
    "Clamp6",
    "FastGELU",
    "LaplaceActivation",
    "QuickGELU",
    "ReLUSquared",
    "cast_activation_type",
    "get_activation",
    "MultiheadAttention",
    "TransformerDecoder",
    "TransformerDecoderLayer",
    "TransformerEncoder",
    "TransformerEncoderLayer",
    "get_attention_mask",
    "nucleus_sampling",
    "BiFPN",
    "BiFPNBlock",
    "MonotonicAttention",
    "monotonic_attention",
    "RwkvAttention",
    "RwkvBlock",
    "RwkvFeedForward",
    "RwkvStack",
    "UNet",
    "detect_device",
    "base_device",
    "cpu_device",
    "gpu_device",
    "metal_device",
    "ConsistencyModel",
    "GaussianDiffusion",
    "cast_beta_schedule",
    "get_diffusion_beta_schedule",
    "BaseODESolver",
    "EulerODESolver",
    "HeunODESolver",
    "RK4ODESolver",
    "cast_solver_type",
    "get_ode_solver",
    "FourierEmbeddings",
    "IdentityPositionalEmbeddings",
    "LearnedPositionalEmbeddings",
    "RotaryEmbeddings",
    "SinusoidalEmbeddings",
    "apply_rotary_embeddings",
    "cast_embedding_kind",
    "fourier_embeddings",
    "get_positional_embeddings",
    "get_rotary_embeddings",
    "rotary_embeddings",
    "StreamingConv1d",
    "StreamingConvTranspose1d",
    "as_numpy_array",
    "as_tensor",
    "recursive_apply",
    "recursive_chunk",
    "set_random_seed",
    "streamable_cbr",
    "streaming_add",
    "streaming_conv_1d",
    "streaming_conv_transpose_1d",
    "init_",
    "KMeans",
    "kmeans_fn",
    "LoraColumnParallelLinear",
    "LoraConv1d",
    "LoraConv2d",
    "LoraConvTranspose1d",
    "LoraConvTranspose2d",
    "LoraEmbedding",
    "LoraGRU",
    "LoraGRUCell",
    "LoraLSTM",
    "LoraLSTMCell",
    "LoraLinear",
    "LoraParallelEmbedding",
    "LoraRowParallelLinear",
    "freeze_non_lora_",
    "lora",
    "maybe_lora",
    "maybe_lora_weight_norm",
    "reset_lora_weights_",
    "ImageGradLoss",
    "LPIPS",
    "MFCCLoss",
    "MelLoss",
    "MultiResolutionSTFTLoss",
    "SSIMLoss",
    "STFTLoss",
    "get_stft_window",
    "kl_div_pair_loss",
    "kl_div_single_loss",
    "log_cosh_loss",
    "log_stft_magnitude_loss",
    "pseudo_huber_loss",
    "spectral_convergence_loss",
    "stft",
    "stft_magnitude_loss",
    "BaseLRScheduler",
    "ConstantLRScheduler",
    "CosineDecayLRScheduler",
    "CosineLRScheduler",
    "LinearLRScheduler",
    "SchedulerAdapter",
    "ConvLayerNorm",
    "LastBatchNorm",
    "cast_norm_type",
    "cast_parametrize_norm_type",
    "get_norm_1d",
    "get_norm_2d",
    "get_norm_3d",
    "get_norm_linear",
    "get_parametrization_norm",
    "Adam",
    "Lion",
    "can_use_foreach",
    "can_use_fused",
    "separate_decayable_params",
    "ColumnParallelLinear",
    "MultiprocessConfig",
    "ParallelConfig",
    "ParallelEmbedding",
    "RowParallelLinear",
    "ddp",
    "dp",
    "fsdp",
    "get_data_worker_info",
    "get_unused_port",
    "launch_subprocesses",
    "split_n_items_across_workers",
    "FiniteScalarQuantization",
    "LookupFreeQuantization",
    "ResidualVectorQuantization",
    "VectorQuantization",
    "BaseLauncher",
    "MultiProcessLauncher",
    "SingleProcessLauncher",
    "LogAudio",
    "LogImage",
    "LogLine",
    "LogVideo",
    "Logger",
    "LoggerImpl",
    "CursesLogger",
    "JsonLogger",
    "StdoutLogger",
    "TensorboardLogger",
    "TorchCompileOptions",
    "CPUStatsOptions",
    "DataLoaderConfig",
    "GPUStatsOptions",
    "ProfilerOptions",
    "Config",
    "Task",
    "collate",
    "collate_non_null",
    "pad_all",
    "pad_sequence",
    "SmallDataset",
    "ErrorHandlingDataset",
    "ErrorHandlingIterableDataset",
    "ExceptionSummary",
    "error_handling_dataset",
    "SquareResizeCrop",
    "UpperLeftCrop",
    "denormalize",
    "make_same_size",
    "make_size",
    "pil_to_tensor",
    "random_square_crop",
    "random_square_crop_multi",
    "square_crop",
    "square_resize_crop",
    "upper_left_crop",
    "add_toast",
    "create_git_bundle",
    "get_git_state",
    "save_config",
    "test_dataset",
    "read_gif",
    "write_gif",
    "configure_logging",
    "TextBlock",
    "colored",
    "format_datetime",
    "format_timedelta",
    "outlined",
    "render_text_blocks",
    "show_error",
    "show_warning",
    "uncolored",
    "wrapped",
    "TokenReader",
    "TokenWriter",
    "token_file",
]

__all__ += [
    "ActivationType",
    "add_toast",
    "EmbeddingKind",
    "NormType",
    "ODESolverType",
    "OptType",
    "ParametrizationNormType",
    "Phase",
    "RwkvAttentionState",
    "RwkvFeedForwardState",
    "RwkvState",
    "Toasts",
]

import os
from typing import TYPE_CHECKING

# If this flag is set, eagerly imports the entire package (not recommended).
IMPORT_ALL = int(os.environ.get("MLFAB_IMPORT_ALL", "0")) != 0

del os

# This dictionary is auto-generated and shouldn't be modified by hand; instead,
# run the update script.
NAME_MAP: dict[str, str] = {
    "UserConfig": "core.conf",
    "field": "core.conf",
    "get_data_dir": "core.conf",
    "get_pretrained_models_dir": "core.conf",
    "get_run_dir": "core.conf",
    "get_stage_dir": "core.conf",
    "load_user_config": "core.conf",
    "State": "core.state",
    "cast_phase": "core.state",
    "Clamp": "nn.activations",
    "Clamp6": "nn.activations",
    "FastGELU": "nn.activations",
    "LaplaceActivation": "nn.activations",
    "QuickGELU": "nn.activations",
    "ReLUSquared": "nn.activations",
    "cast_activation_type": "nn.activations",
    "get_activation": "nn.activations",
    "MultiheadAttention": "nn.architectures.attention",
    "TransformerDecoder": "nn.architectures.attention",
    "TransformerDecoderLayer": "nn.architectures.attention",
    "TransformerEncoder": "nn.architectures.attention",
    "TransformerEncoderLayer": "nn.architectures.attention",
    "get_attention_mask": "nn.architectures.attention",
    "nucleus_sampling": "nn.architectures.attention",
    "BiFPN": "nn.architectures.bifpn",
    "BiFPNBlock": "nn.architectures.bifpn",
    "MonotonicAttention": "nn.architectures.monotonic_attention",
    "monotonic_attention": "nn.architectures.monotonic_attention",
    "RwkvAttention": "nn.architectures.rwkv",
    "RwkvBlock": "nn.architectures.rwkv",
    "RwkvFeedForward": "nn.architectures.rwkv",
    "RwkvStack": "nn.architectures.rwkv",
    "UNet": "nn.architectures.unet",
    "detect_device": "nn.device.auto",
    "base_device": "nn.device.base",
    "cpu_device": "nn.device.cpu",
    "gpu_device": "nn.device.gpu",
    "metal_device": "nn.device.metal",
    "ConsistencyModel": "nn.diffusion.consistency",
    "GaussianDiffusion": "nn.diffusion.gaussian",
    "cast_beta_schedule": "nn.diffusion.gaussian",
    "get_diffusion_beta_schedule": "nn.diffusion.gaussian",
    "BaseODESolver": "nn.diffusion.ode",
    "EulerODESolver": "nn.diffusion.ode",
    "HeunODESolver": "nn.diffusion.ode",
    "RK4ODESolver": "nn.diffusion.ode",
    "cast_solver_type": "nn.diffusion.ode",
    "get_ode_solver": "nn.diffusion.ode",
    "FourierEmbeddings": "nn.embeddings",
    "IdentityPositionalEmbeddings": "nn.embeddings",
    "LearnedPositionalEmbeddings": "nn.embeddings",
    "RotaryEmbeddings": "nn.embeddings",
    "SinusoidalEmbeddings": "nn.embeddings",
    "apply_rotary_embeddings": "nn.embeddings",
    "cast_embedding_kind": "nn.embeddings",
    "fourier_embeddings": "nn.embeddings",
    "get_positional_embeddings": "nn.embeddings",
    "get_rotary_embeddings": "nn.embeddings",
    "rotary_embeddings": "nn.embeddings",
    "StreamingConv1d": "nn.functions",
    "StreamingConvTranspose1d": "nn.functions",
    "as_numpy_array": "nn.functions",
    "as_tensor": "nn.functions",
    "recursive_apply": "nn.functions",
    "recursive_chunk": "nn.functions",
    "set_random_seed": "nn.functions",
    "streamable_cbr": "nn.functions",
    "streaming_add": "nn.functions",
    "streaming_conv_1d": "nn.functions",
    "streaming_conv_transpose_1d": "nn.functions",
    "init_": "nn.init",
    "KMeans": "nn.kmeans",
    "kmeans_fn": "nn.kmeans",
    "LoraColumnParallelLinear": "nn.lora",
    "LoraConv1d": "nn.lora",
    "LoraConv2d": "nn.lora",
    "LoraConvTranspose1d": "nn.lora",
    "LoraConvTranspose2d": "nn.lora",
    "LoraEmbedding": "nn.lora",
    "LoraGRU": "nn.lora",
    "LoraGRUCell": "nn.lora",
    "LoraLSTM": "nn.lora",
    "LoraLSTMCell": "nn.lora",
    "LoraLinear": "nn.lora",
    "LoraParallelEmbedding": "nn.lora",
    "LoraRowParallelLinear": "nn.lora",
    "freeze_non_lora_": "nn.lora",
    "lora": "nn.lora",
    "maybe_lora": "nn.lora",
    "maybe_lora_weight_norm": "nn.lora",
    "reset_lora_weights_": "nn.lora",
    "ImageGradLoss": "nn.losses",
    "LPIPS": "nn.losses",
    "MFCCLoss": "nn.losses",
    "MelLoss": "nn.losses",
    "MultiResolutionSTFTLoss": "nn.losses",
    "SSIMLoss": "nn.losses",
    "STFTLoss": "nn.losses",
    "get_stft_window": "nn.losses",
    "kl_div_pair_loss": "nn.losses",
    "kl_div_single_loss": "nn.losses",
    "log_cosh_loss": "nn.losses",
    "log_stft_magnitude_loss": "nn.losses",
    "pseudo_huber_loss": "nn.losses",
    "spectral_convergence_loss": "nn.losses",
    "stft": "nn.losses",
    "stft_magnitude_loss": "nn.losses",
    "BaseLRScheduler": "nn.lr_schedulers",
    "ConstantLRScheduler": "nn.lr_schedulers",
    "CosineDecayLRScheduler": "nn.lr_schedulers",
    "CosineLRScheduler": "nn.lr_schedulers",
    "LinearLRScheduler": "nn.lr_schedulers",
    "SchedulerAdapter": "nn.lr_schedulers",
    "ConvLayerNorm": "nn.norms",
    "LastBatchNorm": "nn.norms",
    "cast_norm_type": "nn.norms",
    "cast_parametrize_norm_type": "nn.norms",
    "get_norm_1d": "nn.norms",
    "get_norm_2d": "nn.norms",
    "get_norm_3d": "nn.norms",
    "get_norm_linear": "nn.norms",
    "get_parametrization_norm": "nn.norms",
    "Adam": "nn.optimizers",
    "Lion": "nn.optimizers",
    "can_use_foreach": "nn.optimizers",
    "can_use_fused": "nn.optimizers",
    "separate_decayable_params": "nn.optimizers",
    "ColumnParallelLinear": "nn.parallel",
    "MultiprocessConfig": "nn.parallel",
    "ParallelConfig": "nn.parallel",
    "ParallelEmbedding": "nn.parallel",
    "RowParallelLinear": "nn.parallel",
    "ddp": "nn.parallel",
    "dp": "nn.parallel",
    "fsdp": "nn.parallel",
    "get_data_worker_info": "nn.parallel",
    "get_unused_port": "nn.parallel",
    "launch_subprocesses": "nn.parallel",
    "split_n_items_across_workers": "nn.parallel",
    "FiniteScalarQuantization": "nn.quantization.fsq",
    "LookupFreeQuantization": "nn.quantization.lfq",
    "ResidualVectorQuantization": "nn.quantization.vq",
    "VectorQuantization": "nn.quantization.vq",
    "BaseLauncher": "task.launchers.base",
    "MultiProcessLauncher": "task.launchers.multi_process",
    "SingleProcessLauncher": "task.launchers.single_process",
    "LogAudio": "task.logger",
    "LogImage": "task.logger",
    "LogLine": "task.logger",
    "LogVideo": "task.logger",
    "Logger": "task.logger",
    "LoggerImpl": "task.logger",
    "CursesLogger": "task.loggers.curses",
    "JsonLogger": "task.loggers.json",
    "StdoutLogger": "task.loggers.stdout",
    "TensorboardLogger": "task.loggers.tensorboard",
    "TorchCompileOptions": "task.mixins.compile",
    "CPUStatsOptions": "task.mixins.cpu_stats",
    "DataLoaderConfig": "task.mixins.data_loader",
    "GPUStatsOptions": "task.mixins.gpu_stats",
    "ProfilerOptions": "task.mixins.profiler",
    "Config": "task.task",
    "Task": "task.task",
    "collate": "utils.data.collate",
    "collate_non_null": "utils.data.collate",
    "pad_all": "utils.data.collate",
    "pad_sequence": "utils.data.collate",
    "SmallDataset": "utils.data.dataset",
    "ErrorHandlingDataset": "utils.data.error_handling",
    "ErrorHandlingIterableDataset": "utils.data.error_handling",
    "ExceptionSummary": "utils.data.error_handling",
    "error_handling_dataset": "utils.data.error_handling",
    "SquareResizeCrop": "utils.data.transforms",
    "UpperLeftCrop": "utils.data.transforms",
    "denormalize": "utils.data.transforms",
    "make_same_size": "utils.data.transforms",
    "make_size": "utils.data.transforms",
    "pil_to_tensor": "utils.data.transforms",
    "random_square_crop": "utils.data.transforms",
    "random_square_crop_multi": "utils.data.transforms",
    "square_crop": "utils.data.transforms",
    "square_resize_crop": "utils.data.transforms",
    "upper_left_crop": "utils.data.transforms",
    "add_toast": "utils.experiments",
    "create_git_bundle": "utils.experiments",
    "get_git_state": "utils.experiments",
    "save_config": "utils.experiments",
    "test_dataset": "utils.experiments",
    "read_gif": "utils.io",
    "write_gif": "utils.io",
    "configure_logging": "utils.logging",
    "TextBlock": "utils.text",
    "colored": "utils.text",
    "format_datetime": "utils.text",
    "format_timedelta": "utils.text",
    "outlined": "utils.text",
    "render_text_blocks": "utils.text",
    "show_error": "utils.text",
    "show_warning": "utils.text",
    "uncolored": "utils.text",
    "wrapped": "utils.text",
    "TokenReader": "utils.tokens",
    "TokenWriter": "utils.tokens",
    "token_file": "utils.tokens",
}

# Need to manually set some values which can't be auto-generated.
NAME_MAP.update(
    {
        "ActivationType": "nn.activations",
        "add_toast": "utils.experiments",
        "EmbeddingKind": "nn.embeddings",
        "NormType": "nn.norms",
        "ODESolverType": "nn.diffusion.ode",
        "OptType": "task.mixins.optimizer",
        "ParametrizationNormType": "nn.norms",
        "Phase": "core.state",
        "RwkvAttentionState": "nn.architectures.rwkv",
        "RwkvFeedForwardState": "nn.architectures.rwkv",
        "RwkvState": "nn.architectures.rwkv",
        "Toasts": "utils.experiments",
    },
)


def __getattr__(name: str) -> object:
    if name not in NAME_MAP:
        raise AttributeError(f"{__name__} has no attribute {name}")

    module_name = f"mlfab.{NAME_MAP[name]}"
    module = __import__(module_name, fromlist=[name])
    return getattr(module, name)


if IMPORT_ALL or TYPE_CHECKING:
    from mlfab.core.conf import (
        UserConfig,
        field,
        get_data_dir,
        get_pretrained_models_dir,
        get_run_dir,
        get_stage_dir,
        load_user_config,
    )
    from mlfab.core.state import Phase, State, cast_phase
    from mlfab.nn.activations import (
        ActivationType,
        Clamp,
        Clamp6,
        FastGELU,
        LaplaceActivation,
        QuickGELU,
        ReLUSquared,
        cast_activation_type,
        get_activation,
    )
    from mlfab.nn.architectures.attention import (
        MultiheadAttention,
        TransformerDecoder,
        TransformerDecoderLayer,
        TransformerEncoder,
        TransformerEncoderLayer,
        get_attention_mask,
        nucleus_sampling,
    )
    from mlfab.nn.architectures.bifpn import BiFPN, BiFPNBlock
    from mlfab.nn.architectures.monotonic_attention import MonotonicAttention, monotonic_attention
    from mlfab.nn.architectures.rwkv import (
        RwkvAttention,
        RwkvAttentionState,
        RwkvBlock,
        RwkvFeedForward,
        RwkvFeedForwardState,
        RwkvStack,
        RwkvState,
    )
    from mlfab.nn.architectures.unet import UNet
    from mlfab.nn.device.auto import detect_device
    from mlfab.nn.device.base import base_device
    from mlfab.nn.device.cpu import cpu_device
    from mlfab.nn.device.gpu import gpu_device
    from mlfab.nn.device.metal import metal_device
    from mlfab.nn.diffusion.consistency import ConsistencyModel
    from mlfab.nn.diffusion.gaussian import GaussianDiffusion, cast_beta_schedule, get_diffusion_beta_schedule
    from mlfab.nn.diffusion.ode import (
        BaseODESolver,
        EulerODESolver,
        HeunODESolver,
        ODESolverType,
        RK4ODESolver,
        cast_solver_type,
        get_ode_solver,
    )
    from mlfab.nn.embeddings import (
        EmbeddingKind,
        FourierEmbeddings,
        IdentityPositionalEmbeddings,
        LearnedPositionalEmbeddings,
        RotaryEmbeddings,
        SinusoidalEmbeddings,
        apply_rotary_embeddings,
        cast_embedding_kind,
        fourier_embeddings,
        get_positional_embeddings,
        get_rotary_embeddings,
        rotary_embeddings,
    )
    from mlfab.nn.functions import (
        StreamingConv1d,
        StreamingConvTranspose1d,
        as_numpy_array,
        as_tensor,
        recursive_apply,
        recursive_chunk,
        set_random_seed,
        streamable_cbr,
        streaming_add,
        streaming_conv_1d,
        streaming_conv_transpose_1d,
    )
    from mlfab.nn.init import init_
    from mlfab.nn.kmeans import KMeans, kmeans_fn
    from mlfab.nn.lora import (
        LoraColumnParallelLinear,
        LoraConv1d,
        LoraConv2d,
        LoraConvTranspose1d,
        LoraConvTranspose2d,
        LoraEmbedding,
        LoraGRU,
        LoraGRUCell,
        LoraLinear,
        LoraLSTM,
        LoraLSTMCell,
        LoraParallelEmbedding,
        LoraRowParallelLinear,
        freeze_non_lora_,
        lora,
        maybe_lora,
        maybe_lora_weight_norm,
        reset_lora_weights_,
    )
    from mlfab.nn.losses import (
        LPIPS,
        ImageGradLoss,
        MelLoss,
        MFCCLoss,
        MultiResolutionSTFTLoss,
        SSIMLoss,
        STFTLoss,
        get_stft_window,
        kl_div_pair_loss,
        kl_div_single_loss,
        log_cosh_loss,
        log_stft_magnitude_loss,
        pseudo_huber_loss,
        spectral_convergence_loss,
        stft,
        stft_magnitude_loss,
    )
    from mlfab.nn.lr_schedulers import (
        BaseLRScheduler,
        ConstantLRScheduler,
        CosineDecayLRScheduler,
        CosineLRScheduler,
        LinearLRScheduler,
        SchedulerAdapter,
    )
    from mlfab.nn.norms import (
        ConvLayerNorm,
        LastBatchNorm,
        NormType,
        ParametrizationNormType,
        cast_norm_type,
        cast_parametrize_norm_type,
        get_norm_1d,
        get_norm_2d,
        get_norm_3d,
        get_norm_linear,
        get_parametrization_norm,
    )
    from mlfab.nn.optimizers import Adam, Lion, can_use_foreach, can_use_fused, separate_decayable_params
    from mlfab.nn.parallel import (
        ColumnParallelLinear,
        MultiprocessConfig,
        ParallelConfig,
        ParallelEmbedding,
        RowParallelLinear,
        ddp,
        dp,
        fsdp,
        get_data_worker_info,
        get_unused_port,
        launch_subprocesses,
        split_n_items_across_workers,
    )
    from mlfab.nn.quantization.fsq import FiniteScalarQuantization
    from mlfab.nn.quantization.lfq import LookupFreeQuantization
    from mlfab.nn.quantization.vq import ResidualVectorQuantization, VectorQuantization
    from mlfab.task.launchers.base import BaseLauncher
    from mlfab.task.launchers.multi_process import MultiProcessLauncher
    from mlfab.task.launchers.single_process import SingleProcessLauncher
    from mlfab.task.logger import LogAudio, Logger, LoggerImpl, LogImage, LogLine, LogVideo
    from mlfab.task.loggers.curses import CursesLogger
    from mlfab.task.loggers.json import JsonLogger
    from mlfab.task.loggers.stdout import StdoutLogger
    from mlfab.task.loggers.tensorboard import TensorboardLogger
    from mlfab.task.mixins.compile import TorchCompileOptions
    from mlfab.task.mixins.cpu_stats import CPUStatsOptions
    from mlfab.task.mixins.data_loader import DataLoaderConfig
    from mlfab.task.mixins.gpu_stats import GPUStatsOptions
    from mlfab.task.mixins.optimizer import OptType
    from mlfab.task.mixins.profiler import ProfilerOptions
    from mlfab.task.task import Config, Task
    from mlfab.utils.data.collate import collate, collate_non_null, pad_all, pad_sequence
    from mlfab.utils.data.dataset import SmallDataset
    from mlfab.utils.data.error_handling import (
        ErrorHandlingDataset,
        ErrorHandlingIterableDataset,
        ExceptionSummary,
        error_handling_dataset,
    )
    from mlfab.utils.data.transforms import (
        SquareResizeCrop,
        UpperLeftCrop,
        denormalize,
        make_same_size,
        make_size,
        pil_to_tensor,
        random_square_crop,
        random_square_crop_multi,
        square_crop,
        square_resize_crop,
        upper_left_crop,
    )
    from mlfab.utils.experiments import Toasts, add_toast, create_git_bundle, get_git_state, save_config, test_dataset
    from mlfab.utils.io import read_gif, write_gif
    from mlfab.utils.logging import configure_logging
    from mlfab.utils.text import (
        TextBlock,
        colored,
        format_datetime,
        format_timedelta,
        outlined,
        render_text_blocks,
        show_error,
        show_warning,
        uncolored,
        wrapped,
    )
    from mlfab.utils.tokens import TokenReader, TokenWriter, token_file

del TYPE_CHECKING, IMPORT_ALL
