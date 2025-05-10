# パルス測定プログラム

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from src.gui import Application
from src.database._commands import initialize_db
from src.database.models import MeasureType
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def append_record_measure_types():
    """
    測定タイプをデータベースに追加
    """
    session = Session()
    try:
        measure_types = ["NARMA", "2-terminal I-Vsweep", "2-terminal Pulse"]
        for measure_type in measure_types:
            if not session.query(MeasureType).filter_by(name=measure_type).first():
                session.add(MeasureType(name=measure_type))
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error appending measure types: {e}")
    finally:
        session.close()

def main():
    # データベースの初期化
    initialize_db()
    append_record_measure_types()

    # GUIアプリケーションの起動
    root = tk.Tk()
    #root.geometry("530x300")
    #root.resizable(False, False)#ウィンドウサイズをフリーズ
    root.lift()#最前面に表示
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()