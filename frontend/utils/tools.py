OPTION_MENU_STYLE = {
    "container": {"padding": "5!important", "background-color": "black"},
    "icon": {"color": "white", "font-size": "23px"},
    "nav-link": {
        "color": "white",
        "font-size": "20px",
        "text-align": "left",
        "margin": "0px",
        "--hover-color": "blue",
    },
    "nav-link-selected": {"background-color": "#02ab21"},
}

OPTION_MENU_ICONS = [
    "house-fill",
    # "chat-fill",
    "person-circle",
    "trophy-fill",
    "chat-fill",
    "info-circle-fill",
]

OPTION_MENU_ITEMS = ["Home", "Dashboard", "Charts"]

QUERY_FIELDS = {
    "symbol": 1,
    "open": 1,
    "close": 1,
    "time": 1,
    "low": 1,
    "high": 1,
    "volume": 1,
    "_id": 0,
}

SYMBOLS = ["MSFT", "GOOG", "TSLA", "AMZN", "FB", "^GSPC"]

COLUMNS_CHART = ["time", "low", "high", "close", "open", "volume"]
