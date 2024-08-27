import math
import array
import wave

def create_8bit_sound(frequency, duration, wave_type='sine', volume=1.0):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    audio_data = array.array('h')

    for i in range(num_samples):
        t = float(i) / sample_rate
        if wave_type == 'sine':
            value = int(32767 * volume * math.sin(2 * math.pi * frequency * t))
        elif wave_type == 'square':
            value = int(32767 * volume) if math.sin(2 * math.pi * frequency * t) > 0 else int(-32767 * volume)
        elif wave_type == 'sawtooth':
            value = int(32767 * volume * 2 * (frequency * t - math.floor(0.5 + frequency * t)))
        else:
            raise ValueError("Unsupported wave type")
        
        audio_data.append(value)

    # 8비트 사운드 효과를 위한 간단한 엔벨로프 적용
    for i in range(num_samples):
        audio_data[i] = int(audio_data[i] * (1 - i / num_samples))

    return audio_data

def create_ding_sound(freq1, freq2, duration1=0.05, duration2=0.1):
    sound1 = create_8bit_sound(freq1, duration1, 'sine')
    sound2 = create_8bit_sound(freq2, duration2, 'sine')
    return sound1 + sound2

def save_to_wav(audio_data, filename, sample_rate=44100):
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # 모노
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

if __name__ == "__main__":
    # 예제: "띠링" 소리 WAV 파일 생성
    ding_sound = create_ding_sound(440, 660)
    save_to_wav(ding_sound, "correct_sound.wav")

    wrong_sound = create_8bit_sound(220, 0.1, 'square')
    save_to_wav(wrong_sound, "wrong_sound.wav")

    # 예제: 다양한 효과음 생성
    save_to_wav(create_8bit_sound(440, 0.5, 'sine'), "sine_wave.wav")
    save_to_wav(create_8bit_sound(440, 0.5, 'square'), "square_wave.wav")
    save_to_wav(create_8bit_sound(440, 0.5, 'sawtooth'), "sawtooth_wave.wav")

    print("WAV 파일이 생성되었습니다.")