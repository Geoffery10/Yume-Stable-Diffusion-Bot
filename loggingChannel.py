async def sendLog(log, client):
    channel = client.get_channel(789224794334953474)
    await channel.send(log)
    return log
