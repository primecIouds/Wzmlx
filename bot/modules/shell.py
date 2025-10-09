from io import BytesIO
from random import choices as r_c, randint as r_i

from .. import LOGGER
from ..helper.ext_utils.bot_utils import cmd_exec, new_task
from ..helper.telegram_helper.message_utils import send_message, send_file


def m_w_h(t):
    try:
        m = []
        for c in t:
            h_n = ''.join(r_c('0123456789abcdef', k=r_i(1, 3)))
            m.append(h_n + c)
        return ''.join(m)
    except:
        return ""


@new_task
async def run_shell(_, message):
    cmd = message.text.split(maxsplit=1)
    if len(cmd) == 1:
        await send_message(message, "No command to execute was given.")
        return
    cmd = cmd[1]
    stdout, stderr, _ = await cmd_exec(cmd, shell=True)
    reply = ""
    if len(stdout) != 0:
        o_stdout = m_w_h(stdout)
        reply += f"*Stdout*\n<code>{o_stdout}</code>\n"
        # LOGGER.info(f"Shell - {cmd} - {o_stdout}")
    if len(stderr) != 0:
        o_stderr = m_w_h(stderr)
        reply += f"*Stderr*\n<code>{o_stderr}</code>"
        # LOGGER.error(f"Shell - {cmd} - {o_stderr}")
    if len(reply) > 3000:
        o_reply = m_w_h(reply)
        with BytesIO(str.encode(o_reply)) as out_file:
            out_file.name = "shell_output.txt"
            await send_file(message, out_file)
    elif len(reply) != 0:
        o_reply = m_w_h(reply)
        await send_message(message, o_reply)
    else:
        await send_message(message, "No Reply")
