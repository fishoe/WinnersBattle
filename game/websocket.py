from .models import Player, Match
import json

async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        # handshake
        if event['type'] == 'websocket.connect':
            await send({
                'type': 'websocket.accept'
            })

        # disconnected
        if event['type'] == 'websocket.disconnect':
            msg = json.loads(event['text'])
            pId = int(msg[pId])
            idx, pos = matching.findBypId(pId)
            if idx != -1:
                t = matching[idx].stopMatch(pos)
                del t
            break

        # receive
        if event['type'] == 'websocket.receive':
            msg = json.loads(event['text'])
            print(msg)
            # login
            if msg['stat'] == "0":
                try:
                    pId = Player.objects.get(name=msg['id'], password=msg['pw'])
                except Player.DoesNotExist:
                    await send({
                        'type': 'websocket.close',
                        'text': 'Wrong Information'
                    })
                    break

                if matching.waiting:
                    await matching.list[-1].join(pId, send)
                else:
                    matching.list.append(matching(pId, send))
                    await send({'type': 'websocket.send',
                          'text': json.dumps({
                              'stat': '2'
                          })})

                print("login Success : {}".format(pId))
            # getHand
            elif msg['stat'] == "1":
                no = int(msg['matchNo'])
                hand = int(msg['hand'])
                idx = matching.findByNo(no)
                matching.list[idx].getHand(id,hand)
                print("{}:hand-in :".format(idx) + msg['matchNo'] + " - "+msg['hand'])


class matching():
    list = []
    counter = 0
    waiting = False

    def __init__(self, hostId, send):
        waiting = True
        self.host = hostId
        self.hostHand = -1
        self.guestHand = -1
        self.hSoc = send
        self.no = matching.counter
        matching.counter += 1
        matching.list.append(self)

    def __del__(self):
        matching.list.remove(self)

    async def join(self, guestName, send):
        self.guest = guestName
        self.gSoc = send
        waiting = False

        gd={'type':'websocket.send',
            'text': json.dumps({
                'stat' : '1',
                'matchNo': self.no,
                'pId':self.guest
            })}
        hd={'type':'websocket.send',
            'text':json.dumps({
                'stat': '1',
                'matchNo': self.no,
                'pId': self.guest
            })}

        self.hSoc(hd)
        self.gSoc(gd)


    async def stopMatch(self, pos):
        if pos == 0:
            p = Match(winner=self.guest, loser=self.host)
            p.save()
            d = {
                'type': 'websocket.send',
                'text': json.dumps({
                    'stat': '0',
                    'winner': '{}'.format(self.guest)
                })
            }
            await self.gSoc(d)
        else:
            p = Match(winner=self.host, loser=self.guest)
            p.save()
            d = {
                'type': 'websocket.send',
                'text' : json.dumps({
                    'stat': '0',
                    'winner': '{}'.format(self.host)
                })
            }
            await self.hSoc(d)

    async def getHand(self, pId, hand):
        if self.host == pId:
            self.hostHand = hand
        elif self.guest == pId:
            self.guestHand = hand

        if self.host != -1 and self.guest != -1:
            winner = None
            loser = None
            winHand = 0
            loseHand = 0
            draw = -1

            # judgeLogic
            if self.hostHand == self.guestHand:
                winHand = self.host
                loseHand = self.guest
                draw = self.hostHand
            elif self.hostHand == 0:
                winner = self.guest
                winHand = self.guestHand
                loser = self.host
                draw = 0
            elif self.guestHand == 0:
                winner = self.host
                winHand = self.hostHand
                loser = self.guest
                draw = 0
            elif (self.guestHand == 1 and self.hostHand == 2) or (self.guestHand == 2 and self.hostHand == 3) or (
                    self.guestHand == 3 and self.hostHand == 1):
                winner = self.guest
                winHand = self.guestHand
                loser = self.host
                loseHand = self.hostHand
            else:
                winner = self.host
                winHand = self.hostHand
                loser = self.guest
                loseHand = self.guestHand

            m=Match(Winner=winner,Loser=loser,win_hand=winHand,lose_hand=loseHand,draw_hand=draw)
            m.save()

            d = {
                'type': 'websocket.send',
                'text' : json.dumps({
                    'stat': '0',
                    'winner': '{}'.format(winner)
                })
            }
            await self.hSoc(d)
            await self.gSoc(d)

    @classmethod
    def findByNo(cls, no):
        for idx, it in enumerate(cls.list):
            if no == it.no:
                return idx
        return -1

    @classmethod
    def findBypId(cls, pId):
        for idx, it in enumerate(cls.list):
            if it.guest == pId:
                return idx, 1
            elif it.host == pId:
                return idx, 0
        return -1, -1
