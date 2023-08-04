import dotenv, os, json, gspread


dotenv.load_dotenv()


SERVICE_ACCOUNT = json.loads(os.getenv('SERVICE_ACCOUNT'))

SHEET_NAME = os.getenv('SHEET_NAME')
LIST_FREQ_NAME = os.getenv('LIST_FREQ')
LIST_CREQ_NAME = os.getenv('LIST_CREQ')
LIST_KEYW_NAME = os.getenv('LIST_KEYW')


gc = gspread.service_account_from_dict(SERVICE_ACCOUNT)

SHEET = gc.open_by_key(SHEET_NAME)

LIST_FREQ = SHEET.worksheet(LIST_FREQ_NAME)
LIST_CREQ = SHEET.worksheet(LIST_CREQ_NAME)
LIST_KEYW = SHEET.worksheet(LIST_KEYW_NAME)

