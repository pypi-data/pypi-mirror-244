from numpy import pi
from waveforms.waveform import Waveform, cos, sin, step, zero

from .base import AWGChannel, Capture, Context, MultAWGChannel, QLispError


def _set_bias(ctx: Context, channel: str, bias: float | tuple):
    if isinstance(bias, tuple):
        bias, edge, buffer = bias
    else:
        edge, buffer = 0, 0
    if ctx.biases[channel] != bias:
        _, *qubits = channel
        t = max(ctx.time[q] for q in qubits)
        wav = (bias - ctx.biases[channel]) * step(edge) >> (t + buffer / 2)
        _play(ctx, channel, wav)
        ctx.biases[channel] = bias


def _add_bias(ctx: Context, channel: str, bias: float | tuple):
    if isinstance(bias, tuple):
        bias, edge, buffer = bias
        _set_bias(ctx, channel, (bias + ctx.biases[channel], edge, buffer))
    else:
        _set_bias(ctx, channel, bias)


def _set_time(ctx: Context, target: tuple, time: float):
    from waveforms.waveform import NDIGITS
    ctx.time[target] = round(time, NDIGITS)


def _add_time(ctx: Context, target: tuple, time: float):
    from waveforms.waveform import NDIGITS
    ctx.time[target] = round(ctx.time[target] + time, NDIGITS)


def _set_phase(ctx: Context, target: tuple, phase: float):
    ctx.phases_ext[target][1] = phase + ctx.phases_ext[target][0]


def _add_phase(ctx: Context, target: tuple, phase: float):
    ctx.phases_ext[target][1] += phase


def _set_phase_ext(ctx: Context, target: tuple, level: int, phase: float):
    ctx.phases_ext[target][level] = phase


def _add_phase_ext(ctx: Context, target: tuple, level: int, phase: float):
    ctx.phases_ext[target][level] += phase


def _play(ctx: Context, channel: tuple, wav: Waveform):
    if wav is zero():
        return
    name, *qubits = channel
    ch = ctx.get_awg_channel(name, qubits)
    print(type(ch), ch)
    if isinstance(ch, AWGChannel):
        ctx.waveforms[ch.name].append(wav)
    else:
        _mult_channel_play(ctx, wav, ch)


def _mult_channel_play(ctx: Context, wav, ch: MultAWGChannel):
    lofreq = ch.lo_freq
    if ch.I is not None:
        I = (2 * wav * cos(-2 * pi * lofreq)).filter(high=2 * pi * lofreq)
        ctx.waveforms[ch.I.name].append(I)
    if ch.Q is not None:
        Q = (2 * wav * sin(-2 * pi * lofreq)).filter(high=2 * pi * lofreq)
        ctx.waveforms[ch.Q.name].append(Q)


def _capture(ctx: Context, cbit: tuple[str, int], info: Capture):
    hardware = ctx.get_ad_channel(info.qubit)
    name, index = cbit
    ctx.measures[name][index] = Capture(info.qubit, cbit, info.time,
                                        info.signal, info.params, hardware)


def execute(ctx: Context, cmd: tuple[tuple, tuple | str]):

    (op, *args), target = cmd
    dispatch = {
        '!nop': lambda *args, **kw: None,
        '!set_time': _set_time,
        '!set_phase': _set_phase,
        '!set_phase_ext': _set_phase_ext,
        '!set_bias': _set_bias,
        '!play': _play,
        '!capture': _capture,
        '!add_time': _add_time,
        '!add_phase': _add_phase,
        '!add_phase_ext': _add_phase_ext,
        '!add_bias': _add_bias,
    }

    if op in dispatch:
        dispatch[op](ctx, target, args[0])
    else:
        raise QLispError(f'Unknown command: {cmd}')
