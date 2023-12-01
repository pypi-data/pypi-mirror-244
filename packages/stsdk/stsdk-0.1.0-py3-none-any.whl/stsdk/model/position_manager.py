from stsdk.common.key import ORDER_DIRECTION_BUY_STR


class PositionModule(object):
    def __init__(
        self,
        long_opening=0.0,
        long_filled=0.0,
        long_outstanding=0.0,
        short_opening=0.0,
        short_filled=0.0,
        short_outstanding=0.0,
    ):
        self.long_opening = long_opening
        self.long_filled = long_filled
        self.long_outstanding = long_outstanding
        self.short_opening = short_opening
        self.short_filled = short_filled
        self.short_outstanding = short_outstanding
        self.log_file = None

    def __str__(self):
        return (
            f"long_opening: {self.long_opening}, long_filled: {self.long_filled}, "
            f"long_outstanding: {self.long_outstanding}, "
            f"short_opening: {self.short_opening}, short_filled: {self.short_filled}, "
            f"short_outstanding: {self.short_outstanding}"
        )

    @property
    def net_position(self):
        return self.long_filled - self.short_filled

    @property
    def net_outstanding_qty(self):
        return self.long_outstanding - self.short_outstanding

    def init_log_file(self, date, symbol, param_num):
        pass

    def clear(self):
        self.long_opening = 0.0
        self.long_filled = 0.0
        self.long_outstanding = 0.0
        self.short_opening = 0.0
        self.short_filled = 0.0
        self.short_outstanding = 0.0
        self.log_file = None

    def record_position(self, position_info):
        """
        position management in PositionModule
        :param position_info, a dictionary with keys as position_record_header
        :return:
        """
        pass


class PositionManager(object):
    def __init__(self):
        self.positions = dict()

    def update_new_position(self, data):
        if "OrderDirection" in data:
            if data["OrderDirection"] == ORDER_DIRECTION_BUY_STR:
                return PositionModule(long_opening=float(data["OriginQuantity"]))
            else:
                return PositionModule(short_opening=float(data["OriginQuantity"]))

    def update_canceled_position(self, data):
        if "OrderDirection" in data:
            if data["OrderDirection"] == ORDER_DIRECTION_BUY_STR:
                return PositionModule(
                    long_opening=-(
                        float(data["OriginQuantity"]) - float(data["FilledQuantity"])
                    ),
                    long_filled=float(data["FilledQuantity"]),
                )
            else:
                return PositionModule(
                    short_opening=-(
                        float(data["OriginQuantity"]) - float(data["FilledQuantity"])
                    ),
                    short_filled=float(data["FilledQuantity"]),
                )

    def update_filled_position(self, data):
        if "OrderDirection" in data:
            if data["OrderDirection"] == ORDER_DIRECTION_BUY_STR:
                return PositionModule(
                    long_opening=-float(data["FilledQuantity"]),
                    long_filled=float(data["FilledQuantity"]),
                )
            else:
                return PositionModule(
                    short_opening=-float(data["FilledQuantity"]),
                    short_filled=float(data["FilledQuantity"]),
                )

    def update_position(self, instrumentId, position):
        if instrumentId not in self.positions:
            self.positions[instrumentId] = PositionModule()
        self.positions[instrumentId].long_opening += position.long_opening
        self.positions[instrumentId].long_filled += position.long_filled
        self.positions[instrumentId].long_outstanding += position.long_outstanding
        self.positions[instrumentId].short_opening += position.short_opening
        self.positions[instrumentId].short_filled += position.short_filled
        self.positions[instrumentId].short_outstanding += position.short_outstanding

    def clear_position(self, instrumentId):
        self.positions[instrumentId].clear()

    def get_position(self, instrumentId):
        return self.positions.get(instrumentId, PositionModule())

    def get_all_positions(self):
        return self.positions
