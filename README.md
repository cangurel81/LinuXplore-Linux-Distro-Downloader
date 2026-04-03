# LinuXplore - Linux Distro Downloader

A modern desktop application to discover and download Linux distributions.

![LinuXplore](linux.png)

## Features

- **50+ Linux Distributions** - Most popular Linux distros
- **Category Filtering** - Daily use, security, lightweight, server
- **Fast Download** - Download large files securely
- **USB Writing** - Write to USB with Rufus or Etcher
- **Multi-language** - Turkish and English support
- **Repology API** - Auto-update with latest versions

## Supported Distributions

- Ubuntu, Linux Mint, Fedora, Debian, Arch Linux
- Kali Linux, Parrot OS, Tails (Security)
- MX Linux, antiX, Puppy Linux (Lightweight)
- Rocky Linux, AlmaLinux, openSUSE (Server)
- And more...

## Download

### Ready-to-Use EXE (Recommended)
- [LinuXplore.exe]- Ready to run for Windows

### Run from Source Code

#### Requirements

- Python 3.10+
- Windows 10/11

#### Installation

1. Clone the repository:
```bash
git clone https://github.com/cangurel81/LinuXplore-Linux-Distro-Downloader
cd linuxplore
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Download Distribution
1. Select a distribution
2. Click "Download" button
3. Choose download folder
4. Track download progress

### Write to USB
1. Click Rufus or Etcher buttons
2. Select downloaded ISO
3. Write to your USB drive

### Filter by Category
- **All** - All distributions
- **Lightweight (Old PC)** - For low-resource systems
- **Daily Use** - For home users
- **Pentest (Security)** - For security testing
- **Server** - Server distributions

## Technologies

- **Python 3** - Main programming language
- **Flet** - Modern cross-platform UI framework
- **Requests** - HTTP requests
- **Repology API** - Distribution version info

## Project Structure

```
linuXplore/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── linux.ico            # Application icon
├── linux.png            # Logo
├── src/
│   ├── ui/
│   │   └── app_ui.py   # User interface
│   ├── logic/
│   │   ├── scraper.py    # Repology API scraper
│   │   └── downloader.py # ISO downloader
│   └── data/
│       ├── distros.json  # Distribution data
│       └── locales.json  # Language files
└── README.md           # This file
```

## Contributing

1. Fork the repo
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Commit (`git commit -m 'New feature added'`)
5. Push (`git push origin feature/new-feature`)
6. Create Pull Request

## License

GNU General Public License v3.0 - See LICENSE file for details.

## Contact

- Website: [WebAdHere](https://webadhere.com)

---

Made with ❤️ for Linux community

---

# LinuXplore - Linux Dağıtım İndirici

Linux dağıtımlarını keşfetmek ve indirmek için modern bir masaüstü uygulaması.

![LinuXplore](linux.png)

## Özellikler

- **50+ Linux Dağıtım** - En popüler Linux dağıtımları
- **Kategori Filtreleme** - Günlük kullanım, güvenlik, hafif, sunucu
- **Hızlı İndirme** - Büyük dosyaları güvenli şekilde indirin
- **USB Yazma** - Rufus veya Etcher ile USB'ye yazın
- **Çoklu Dil** - Türkçe ve İngilizce destek
- **Repology API** - Otomatik güncelleme ile en güncel sürümler

## Desteklenen Dağıtımlar

- Ubuntu, Linux Mint, Fedora, Debian, Arch Linux
- Kali Linux, Parrot OS, Tails (Güvenlik)
- MX Linux, antiX, Puppy Linux (Hafif)
- Rocky Linux, AlmaLinux, openSUSE (Sunucu)
- Ve daha fazlası...

## İndirme

### Hazır EXE İndir (Önerilen)
- [LinuXplore.exe]Windows için hazır çalıştırılabilir

### Kaynak Koddan Çalıştırma

#### Gereksinimler

- Python 3.10+
- Windows 10/11

#### Kurulum Adımları

1. Repoyu klonlayın:
```bash
git clone https://github.com/cangurel81/LinuXplore-Linux-Distro-Downloader
cd linuxplore
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
python main.py
```

## Kullanım

### Dağıtım İndirme
1. Bir dağıtım seçin
2. "İndir" butonuna tıklayın
3. İndirme klasörü seçin
4. İndirme ilerlemesini takip edin

### USB'ye Yazma
1. Rufus veya Etcher butonlarına tıklayın
2. İndirilen ISO dosyasını seçin
3. USB belleğinize yazın

### Kategorilere Göre Filtreleme
- **Hepsi** - Tüm dağıtımlar
- **Hafif (Eski PC)** - Düşük kaynaklı sistemler için
- **Günlük Kullanım** - Ev kullanıcıları için
- **Pentest (Güvenlik)** - Güvenlik testleri için
- **Server** - Sunucu dağıtımları

## Teknolojiler

- **Python 3** - Ana programlama dili
- **Flet** - Modern çapraz platform UI framework
- **Requests** - HTTP istekleri
- **Repology API** - Dağıtım sürüm bilgileri

## Proje Yapısı

```
linuXplore/
├── main.py              # Ana uygulama dosyası
├── requirements.txt     # Python bağımlılıkları
├── linux.ico           # Uygulama ikonu
├── linux.png           # Logo
├── src/
│   ├── ui/
│   │   └── app_ui.py   # Kullanıcı arayüzü
│   ├── logic/
│   │   ├── scraper.py    # Repology API scraper
│   │   └── downloader.py # ISO indirme
│   └── data/
│       ├── distros.json  # Dağıtım verileri
│       └── locales.json  # Dil dosyaları
└── README.md           # Bu dosya
```

## Katkıda Bulunma

1. Fork yapın
2. Yeni bir dal oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi yapın
4. Commit edin (`git commit -m 'Yeni özellik eklendi'`)
5. Dalınızı push edin (`git push origin feature/yeni-ozellik`)
6. Pull Request oluşturun

## Lisans

GNU General Public License v3.0 - Daha fazla bilgi için LICENSE dosyasına bakabilirsiniz.

## İletişim

- Web Sitesi: [WebAdHere](https://webadhere.com)

---

Linux topluluğu için ❤️ ile yapıldı
