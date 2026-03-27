import zipfile
import json

def create_fnf_mod_zip():
    zip_name = "my-cool-mod.zip"
    song_id = "my-song"
    char_id = "my-character"

    print(f"[{zip_name}] の作成を開始します...")

    # テキスト系のファイルデータ
    text_files = {
        f"mods/characters/{char_id}.json": {
            "animations": [
                {"loop": False, "offsets": [0, 0], "fps": 24, "anim": "idle", "name": "Idle", "indices": []},
                {"loop": False, "offsets": [0, 0], "fps": 24, "anim": "singUP", "name": "Up", "indices": []}
            ],
            "no_antialiasing": False,
            "image": f"characters/{char_id}",
            "position": [0, 0],
            "healthicon": "face",
            "flip_x": False,
            "healthbar_colors": [255, 0, 0],
            "camera_position": [0, 0],
            "sing_duration": 4,
            "scale": 1
        },
        f"mods/songs/{song_id}/Charts/normal.json": {
            "song": {"song": "My Song", "notes": [], "bpm": 150, "needsVoices": True, "speed": 2.2, "player1": "bf", "player2": char_id}
        },
        f"mods/songs/{song_id}/Charts/hard.json": {
            "song": {"song": "My Song", "notes": [], "bpm": 150, "needsVoices": True, "speed": 2.8, "player1": "bf", "player2": char_id}
        },
        f"mods/data/{song_id}/events.json": {
            "events": []
        }
    }

    # Luaスクリプト
    lua_script = f"""function onCreate()
    -- MOD読み込み時の処理
    debugPrint('Custom Script Loaded!')
end

function onUpdate(elapsed)
    -- 毎フレームの処理（ギミック用）
end
"""

    # ダミーのバイナリデータ（1x1の透明PNG画像と、無音の音声ファイル用）
    dummy_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n\x2d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    dummy_audio = b''

    # ZIPファイルの生成
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
        # JSONファイルの書き込み
        for path, data in text_files.items():
            z.writestr(path, json.dumps(data, indent=4))
        
        # Luaスクリプトの書き込み
        z.writestr("mods/scripts/custom_script.lua", lua_script)

        # 画像と音声の書き込み
        z.writestr(f"mods/images/characters/{char_id}.png", dummy_png)
        z.writestr(f"mods/songs/{song_id}/Inst.ogg", dummy_audio)
        z.writestr(f"mods/songs/{song_id}/Voices.ogg", dummy_audio)

    print(f"完了しました！同じフォルダ内に '{zip_name}' が作成されています。")

if __name__ == "__main__":
    create_fnf_mod_zip()
