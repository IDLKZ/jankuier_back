from app.shared.dto_constants import DTOConstant


class AlatauCreateResponseOrderDTO:
    ORDER:DTOConstant.StandardOrderStringField(description="ID заказа")
    AMOUNT:DTOConstant.StandardPriceField(description="Сумма заказа")
    CURRENCY:DTOConstant.CurrencyField(description="Валюта")
    MERCHANT:DTOConstant.MerchantIdField(description="ID мерчанта")
    TERMINAL:DTOConstant.TerminalIdField(description="ID терминала")
    DESC:DTOConstant.StandardOrderDescriptionField(description="Описание заказа")
    DESC_ORDER:DTOConstant.StandardNullableFullOrderDescriptionField(description="Описание заказа полное")
    EMAIL:DTOConstant.StandardEmailField(description="Почта клиента")
    WTYPE:DTOConstant.WTypeField(description="Окно оплаты")
    NAME:DTOConstant.StandardNullableVarcharField(description="ФИО Клиента")
    P_SIGN:DTOConstant.StandardPSignField(description="Подпись клиента")

    class Config:
        from_attributes = True