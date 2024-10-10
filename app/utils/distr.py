import asyncio
import json
from aiofiles import open as aio_open


async def update_json(client_id, tg_id, email, file_path='/opt/xray/config.json'):
    # Чтение файла
    async with aio_open(file_path, 'r') as file:
        data = json.loads(await file.read())

    # Обновление данных
    user = {'id': client_id, 'email': email, 'flow': 'xtls-rprx-vision', 'tag': tg_id}
    print(user)
    data['inbounds'][1]['settings']['clients'].append(user)
    data['inbounds'][2]['settings']['clients'].append(user)

    # Запись обновленного файла
    async with aio_open(file_path, 'w') as file:
        await file.write(json.dumps(data, indent=4))


async def get_client_id():
    process = await asyncio.create_subprocess_shell(
        'uuidgen',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    return stdout.decode().strip()


async def restart_xray():
    process = await asyncio.create_subprocess_shell(
        'systemctl restart xray',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if stdout:
        return stdout.decode()
    else:
        return stderr.decode()
