import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    scope: typing.Mapping[str, typing.Any]

    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]


class RestaurantManager:
    def __init__(self):
        self.staff = {}

    def staff_order_pass(self,special):
        for i in self.staff.values():
            if special in i.scope["speciality"]:
                return i

    async def __call__(self, request: Request):

        if request.scope['type'] == 'staff.onduty':
            self.staff[request.scope['id']] = request
        elif request.scope['type'] == 'staff.offduty':
            self.staff.pop(request.scope['id'])
        elif request.scope['type'] == 'order':
            found = self.staff_order_pass(special=request.scope["speciality"])
            full_order = await request.receive()
            await found.send(full_order)
            result = await found.receive()
            await request.send(result)
