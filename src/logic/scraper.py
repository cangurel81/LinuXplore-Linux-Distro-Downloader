import requests
import json
import os
import time

class DistroScraper:
    def __init__(self):
        self.repology_api = "https://repology.org/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "LinuXplore/1.0 (https://github.com/linuxplore)"
        })
        
        self.main_distros = {
            "linuxmint": {"Name": "Linux Mint", "Category": "Gunluk Kullanim", "Website": "https://linuxmint.com", "Download": "https://linuxmint.com/download.php"},
            "ubuntu": {"Name": "Ubuntu", "Category": "Gunluk Kullanim", "Website": "https://ubuntu.com", "Download": "https://ubuntu.com/download/desktop"},
            "fedora": {"Name": "Fedora", "Category": "Gunluk Kullanim", "Website": "https://fedoraproject.org", "Download": "https://fedoraproject.org/workstation/download"},
            "debian": {"Name": "Debian", "Category": "Server", "Website": "https://debian.org", "Download": "https://debian.org/CD/http-ftp/"},
            "arch": {"Name": "Arch Linux", "Category": "Server", "Website": "https://archlinux.org", "Download": "https://archlinux.org/download/"},
            "linuxlite": {"Name": "Linux Lite", "Category": "Gunluk Kullanim", "Website": "https://linuxliteos.com", "Download": "https://www.linuxliteos.com/download.html"},
            "zorin": {"Name": "Zorin OS", "Category": "Gunluk Kullanim", "Website": "https://zorin.com/os/", "Download": "https://zorin.com/os/download/"},
            "pop": {"Name": "Pop!_OS", "Category": "Gunluk Kullanim", "Website": "https://pop.system76.com", "Download": "https://pop.system76.com"},
            "elementary": {"Name": "elementary OS", "Category": "Gunluk Kullanim", "Website": "https://elementary.io", "Download": "https://elementary.io"},
            "kali": {"Name": "Kali Linux", "Category": "Pentest (Guvenlik)", "Website": "https://kali.org", "Download": "https://kali.org/get-kali/"},
            "parrot": {"Name": "Parrot OS", "Category": "Pentest (Guvenlik)", "Website": "https://parrotsec.org", "Download": "https://parrotsec.org/download/"},
            "tails": {"Name": "Tails", "Category": "Pentest (Guvenlik)", "Website": "https://tails.boum.org", "Download": "https://tails.boum.org/install/"},
            "qubes": {"Name": "Qubes OS", "Category": "Pentest (Guvenlik)", "Website": "https://qubes-os.org", "Download": "https://www.qubes-os.org/downloads/"},
            "manjaro": {"Name": "Manjaro", "Category": "Gunluk Kullanim", "Website": "https://manjaro.org", "Download": "https://manjaro.org/download/"},
            "endeavouros": {"Name": "EndeavourOS", "Category": "Gunluk Kullanim", "Website": "https://endeavouros.com", "Download": "https://endeavouros.com/latest-release/"},
            "garuda": {"Name": "Garuda Linux", "Category": "Gunluk Kullanim", "Website": "https://garudalinux.org", "Download": "https://garudalinux.org/downloads"},
            "mxlinux": {"Name": "MX Linux", "Category": "Hafif (Eski PC)", "Website": "https://mxlinux.org", "Download": "https://mxlinux.org/download-links/"},
            "antix": {"Name": "antiX", "Category": "Hafif (Eski PC)", "Website": "https://antixlinux.com", "Download": "https://antixlinux.com/download/"},
            "puppy": {"Name": "Puppy Linux", "Category": "Hafif (Eski PC)", "Website": "https://puppylinux.com", "Download": "https://puppylinux.com/downloads.php"},
            "slackware": {"Name": "Slackware", "Category": "Server", "Website": "https://slackware.com", "Download": "https://slackware.com/getslack/"},
            "opensuse": {"Name": "openSUSE", "Category": "Server", "Website": "https://opensuse.org", "Download": "https://get.opensuse.org/leap/"},
            "rocky": {"Name": "Rocky Linux", "Category": "Server", "Website": "https://rockylinux.org", "Download": "https://rockylinux.org/download"},
            "almalinux": {"Name": "AlmaLinux", "Category": "Server", "Website": "https://almalinux.org", "Download": "https://almalinux.org/download/"},
            "centos": {"Name": "CentOS", "Category": "Server", "Website": "https://centos.org", "Download": "https://www.centos.org/download/"},
            "gentoo": {"Name": "Gentoo", "Category": "Server", "Website": "https://gentoo.org", "Download": "https://www.gentoo.org/downloads/"},
            "nixos": {"Name": "NixOS", "Category": "Server", "Website": "https://nixos.org", "Download": "https://nixos.org/download.html"},
            "void": {"Name": "Void Linux", "Category": "Server", "Website": "https://voidlinux.org", "Download": "https://voidlinux.org/download/"},
            "freebsd": {"Name": "FreeBSD", "Category": "Server", "Website": "https://freebsd.org", "Download": "https://www.freebsd.org/where/"},
            "deepin": {"Name": "deepin", "Category": "Gunluk Kullanim", "Website": "https://www.deepin.org", "Download": "https://www.deepin.org/en/download/"},
            "neon": {"Name": "KDE neon", "Category": "Gunluk Kullanim", "Website": "https://neon.kde.org", "Download": "https://neon.kde.org/download"},
            "ubuntu-studio": {"Name": "Ubuntu Studio", "Category": "Gunluk Kullanim", "Website": "https://ubuntustudio.org", "Download": "https://ubuntustudio.org/download/"},
            "kubuntu": {"Name": "Kubuntu", "Category": "Gunluk Kullanim", "Website": "https://kubuntu.org", "Download": "https://kubuntu.org/get-kubuntu/"},
            "xubuntu": {"Name": "Xubuntu", "Category": "Gunluk Kullanim", "Website": "https://xubuntu.org", "Download": "https://xubuntu.org/download/"},
            "lubuntu": {"Name": "Lubuntu", "Category": "Hafif (Eski PC)", "Website": "https://lubuntu.org", "Download": "https://lubuntu.org/download/"},
            "popos": {"Name": "Pop!_OS", "Category": "Gunluk Kullanim", "Website": "https://pop.system76.com", "Download": "https://pop.system76.com"},
            "solus": {"Name": "Solus", "Category": "Gunluk Kullanim", "Website": "https://getsol.us", "Download": "https://getsol.us/download/"},
            "mageia": {"Name": "Mageia", "Category": "Gunluk Kullanim", "Website": "https://www.mageia.org", "Download": "https://www.mageia.org/en/get/"},
            "openmandriva": {"Name": "OpenMandriva", "Category": "Gunluk Kullanim", "Website": "https://www.openmandriva.org", "Download": "https://www.openmandriva.org/download/"},
            "tinycore": {"Name": "Tiny Core Linux", "Category": "Hafif (Eski PC)", "Website": "http://www.tinycorelinux.net", "Download": "http://www.tinycorelinux.net/downloads.html"},
            "slax": {"Name": "Slax", "Category": "Hafif (Eski PC)", "Website": "https://www.slax.org", "Download": "https://www.slax.org/download/"},
            "fedoraspin": {"Name": "Fedora Spins", "Category": "Gunluk Kullanim", "Website": "https://spins.fedoraproject.org", "Download": "https://spins.fedoraproject.org"},
            "Nobara": {"Name": "Nobara", "Category": "Gunluk Kullanim", "Website": "https://nobaraproject.org", "Download": "https://nobaraproject.org/downloads/"},
            "fx": {"Name": "FX", "Category": "Gunluk Kullanim", "Website": "https://fxlinux.com", "Download": "https://fxlinux.com/download"},
            "cutefish": {"Name": "CutefishOS", "Category": "Gunluk Kullanim", "Website": "https://cutefish.com", "Download": "https://cutefish.com/download"},
            "whonix": {"Name": "Whonix", "Category": "Pentest (Guvenlik)", "Website": "https://www.whonix.org", "Download": "https://www.whonix.org/download/"},
            "kodachi": {"Name": "Kodachi Linux", "Category": "Pentest (Guvenlik)", "Website": "https://www.dankodachi.com", "Download": "https://www.dankodachi.com/download"},
            "pearlos": {"Name": "Pear OS", "Category": "Gunluk Kullanim", "Website": "https://pearlinux.com", "Download": "https://pearlinux.com/download"},
            "dreamstudio": {"Name": "Dream Studio", "Category": "Gunluk Kullanim", "Website": "https://dreamstudio.com", "Download": "https://dreamstudio.com/download"},
            "kaos": {"Name": "KaOS", "Category": "Gunluk Kullanim", "Website": "https://kaosx.us", "Download": "https://kaosx.us/download"},
            "artix": {"Name": "Artix Linux", "Category": "Gunluk Kullanim", "Website": "https://artixlinux.org", "Download": "https://artixlinux.org/download"},
            "archlabs": {"Name": "ArchLabs", "Category": "Gunluk Kullanim", "Website": "https://archlabslinux.com", "Download": "https://archlabslinux.com/download"},
            "arcolinux": {"Name": "ArcoLinux", "Category": "Gunluk Kullanim", "Website": "https://arcolinux.com", "Download": "https://arcolinux.com/download"},
        }
        
        self.descriptions = {
            "Linux Mint": {"tr": "Yeni kullanıcılara uygun, stabil ve güvenilir masaüstü deneyimi.", "en": "User-friendly, stable and reliable desktop experience."},
            "Ubuntu": {"tr": "Dünyadın en popüler Linux dağıtımlarından biri.", "en": "One of the most popular Linux distributions."},
            "Fedora": {"tr": "En son teknolojileri sunan, geliştirici dostu dağıtım.", "en": "Developer-friendly distribution with latest technologies."},
            "Debian": {"tr": "Özgür yazılım topluluğu tarafından geliştirilen stabil dağıtım.", "en": "Stable distribution developed by free software community."},
            "Arch Linux": {"tr": "Kullanıcının herşeyi kendisi yapılandırdığı rolling dağıtım.", "en": "Rolling release where user configures everything."},
            "Linux Lite": {"tr": "Windows kullanıcıları için tasarlanmış, hafif ve kolay dağıtım.", "en": "Lightweight and easy distribution for Windows users."},
            "Zorin OS": {"tr": "Windows ve macOS'tan geçiş için tasarlanmış dağıtım.", "en": "Distribution designed for Windows and macOS switchers."},
            "Pop!_OS": {"tr": "NVIDIA desteği ve üretkenlik odaklı özelliklerle gelen dağıtım.", "en": "Distribution with NVIDIA support and productivity features."},
            "elementary OS": {"tr": "macOS benzeri zarif tasarımı ile en güzel Linux deneyimlerinden.", "en": "One of the most beautiful Linux experiences with elegant design."},
            "Kali Linux": {"tr": "Sızma testleri ve güvenlik araştırmaları için dağıtım.", "en": "Distribution for penetration testing and security research."},
            "Parrot OS": {"tr": "Güvenlik araştırmaları ve anonimlik için tasarlanmış.", "en": "Designed for security research and anonymity."},
            "Tails": {"tr": "Gizlilik odaklı, RAM'de çalışan taşınabilir işletim sistemi.", "en": "Privacy-focused, RAM-based portable operating system."},
            "Qubes OS": {"tr": "Güvenlik odaklı, her uygulama için izole VM'ler kullanan dağıtım.", "en": "Security-focused distribution using isolated VMs."},
            "Manjaro": {"tr": "Arch Linux gücünü kullanıcı dostu kurulumla sunan dağıtım.", "en": "Arch power with user-friendly installation."},
            "EndeavourOS": {"tr": "Arch Linux'un gücünü kolay kurulumla birleştiren dağıtım.", "en": "Combines Arch Linux power with easy installation."},
            "Garuda Linux": {"tr": "Arch tabanlı, gaming ve modern UI seçenekleriyle gelen dağıtım.", "en": "Arch-based with gaming and modern UI options."},
            "MX Linux": {"tr": "Debian tabanlı, eski PC'ler için ideal hafif dağıtım.", "en": "Debian-based ideal lightweight for old PCs."},
            "antiX": {"tr": "Eski donanımlar için systemd içermeyen hızlı hafif dağıtım.", "en": "Fast lightweight without systemd for old hardware."},
            "Puppy Linux": {"tr": "Tamamen RAM'de çalışabilen inanılmaz küçük dağıtım.", "en": "Incredibly small distribution that runs in RAM."},
            "Slackware": {"tr": "En eski hala aktif Linux dağıtımlarından biri.", "en": "One of the oldest active Linux distributions."},
            "openSUSE": {"tr": "Kurumsal kalite ve topluluk geliştirmesinin birleşimi.", "en": "Enterprise quality combined with community development."},
            "Rocky Linux": {"tr": "RHEL uyumlu kurumsal sunucu dağıtımı.", "en": "RHEL-compatible enterprise server distribution."},
            "AlmaLinux": {"tr": "CentOS devamı RHEL uyumlu kurumsal dağıtım.", "en": "CentOS continuation with RHEL compatibility."},
            "CentOS": {"tr": "Red Hat Enterprise Linux uyumlu kurumsal dağıtım.", "en": "Red Hat Enterprise Linux compatible distribution."},
            "Gentoo": {"tr": "Kaynak koddan derlenen tamamen özelleştirilebilir dağıtım.", "en": "Completely customizable distribution compiled from source."},
            "NixOS": {"tr": "Bildirimci yapılandırma ve tekrarlanabilir sistemler sunar.", "en": "Declarative configuration and reproducible systems."},
            "Void Linux": {"tr": "Runit init sistemi ile minimal ve özelleştirilebilir.", "en": "Minimal and customizable with Runit init system."},
            "FreeBSD": {"tr": "UNIX-benzeri yüksek performanslı işletim sistemi.", "en": "UNIX-like high-performance operating system."},
            "deepin": {"tr": "Modern ve güzel kullanım deneyimi sunan Çin menşeili dağıtım.", "en": "Chinese-origin distribution with modern experience."},
            "KDE neon": {"tr": "En son KDE yazılımları ile güncel masaüstü deneyimi.", "en": "Latest KDE software with up-to-date desktop experience."},
            "Ubuntu Studio": {"tr": "Medya üretimi için optimize edilmiş Ubuntu tabanlı dağıtım.", "en": "Ubuntu-based distribution optimized for media production."},
            "Kubuntu": {"tr": "KDE Plasma masaüstü ile Ubuntu dağıtımı.", "en": "Ubuntu distribution with KDE Plasma desktop."},
            "Xubuntu": {"tr": "XFCE masaüstü ile hafif Ubuntu dağıtımı.", "en": "Lightweight Ubuntu distribution with XFCE desktop."},
            "Lubuntu": {"tr": "LXQt masaüstü ile ultra hafif Ubuntu dağıtımı.", "en": "Ultra lightweight Ubuntu with LXQt desktop."},
            "Solus": {"tr": "Bağımsız, kullanıcı dostu Linux dağıtımı.", "en": "Independent, user-friendly Linux distribution."},
            "Mageia": {"tr": "Mandriva Linux'un topluluk tarafından devam ettirilen versiyonu.", "en": "Mandriva Linux continuation by community."},
            "OpenMandriva": {"tr": "Modern, topluluk destekli Linux dağıtımı.", "en": "Modern community-supported Linux distribution."},
            "Tiny Core Linux": {"tr": "Minimalist, mikroboyutlu Linux dağıtımı.", "en": "Minimalist micro-sized Linux distribution."},
            "Slax": {"tr": "Debian tabanlı, taşınabilir Linux dağıtımı.", "en": "Debian-based portable Linux distribution."},
            "Nobara": {"tr": "Fedora tabanlı, oyuncular için optimize edilmiş dağıtım.", "en": "Fedora-based distribution optimized for gamers."},
            "FX": {"tr": "Kullanıcı deneyimi odaklı Linux dağıtımı.", "en": "Linux distribution focused on user experience."},
            "CutefishOS": {"tr": "Modern ve kullanımı kolay Çin menşeli dağıtım.", "en": "Modern and easy-to-use Chinese-origin distribution."},
            "Whonix": {"tr": "Gizlilik ve anonimlik için tasarlanmış güvenlik dağıtımı.", "en": "Security distribution designed for privacy and anonymity."},
            "Kodachi Linux": {"tr": "Güvenlik ve gizlilik odaklı Debian tabanlı dağıtım.", "en": "Debian-based security and privacy-focused distribution."},
            "Pear OS": {"tr": "macOS benzeri zarif tasarımı ile Linux deneyimi.", "en": "Elegant Linux experience similar to macOS."},
            "Dream Studio": {"tr": "Üretkenlik ve yaratıcılık için tasarlanmış dağıtım.", "en": "Distribution designed for productivity and creativity."},
            "KaOS": {"tr": "KDE Plasma tabanlı bağımsız Linux dağıtımı.", "en": "Independent KDE Plasma based Linux distribution."},
            "Artix Linux": {"tr": "systemd-free Arch tabanlı dağıtım.", "en": "systemd-free Arch-based distribution."},
            "ArchLabs": {"tr": "Arch Linux minimal kurulum ile GNU/Linux deneyimi.", "en": "Arch Linux with minimal setup for GNU/Linux experience."},
            "ArcoLinux": {"tr": "Arch Linux öğrenme ve keşfetme dağıtımı.", "en": "Arch Linux learning and discovery distribution."},
        }
        
        self.icons = {
            "Linux Mint": "M", "Ubuntu": "U", "Fedora": "F", "Debian": "D", "Arch Linux": "A",
            "Kali Linux": "K", "Manjaro": "Mj", "Pop!_OS": "P", "Zorin OS": "Z", "elementary OS": "e",
            "Linux Lite": "L", "MX Linux": "MX", "antiX": "aX", "Puppy Linux": "Pu",
            "openSUSE": "oS", "Rocky Linux": "RL", "AlmaLinux": "AL", "CentOS": "C",
            "Gentoo": "G", "NixOS": "Ni", "Void Linux": "Vo", "FreeBSD": "FB",
            "deepin": "d", "KDE neon": "Ne", "EndeavourOS": "En", "Garuda Linux": "Ga",
            "Tails": "Ta", "Qubes OS": "Q", "Parrot OS": "Pa", "Slackware": "Sl",
            "Ubuntu Studio": "US", "Kubuntu": "Kb", "Xubuntu": "Xb", "Lubuntu": "Lu",
            "Solus": "So", "Mageia": "Ma", "OpenMandriva": "OM", "Tiny Core Linux": "TC",
            "Slax": "Sx", "Nobara": "No", "FX": "FX", "CutefishOS": "CF",
            "Whonix": "Wh", "Kodachi Linux": "Ko",
            "Pear OS": "Pe", "Dream Studio": "DS", "KaOS": "Ka",
            "Artix Linux": "Ar", "ArchLabs": "AL", "ArcoLinux": "Ac",
        }

    def fetch_repology(self):
        distros = []
        projects = list(self.main_distros.keys())
        
        print(f"\n=== Repology API ile {len(projects)} dağıtım güncelleniyor ===\n")
        
        for i, project in enumerate(projects):
            try:
                url = f"{self.repology_api}/project/{project}"
                resp = self.session.get(url, timeout=15)
                
                if resp.status_code == 200:
                    data = resp.json()
                    info = self.main_distros[project]
                    
                    desc = self.descriptions.get(info["Name"], {"tr": info["Name"], "en": info["Name"]})
                    
                    version = self._get_latest_version(data)
                    
                    distro = {
                        "id": project,
                        "name": info["Name"],
                        "description_tr": desc["tr"],
                        "description_en": desc["en"],
                        "category": info["Category"],
                        "website_url": info["Website"],
                        "download_url": info["Download"],
                        "version": version,
                        "hardware": self._get_hardware_req(info["Category"]),
                        "icon_text": self.icons.get(info["Name"], info["Name"][0]),
                        "best_of_year": project in ["linuxmint", "ubuntu", "fedora", "debian", "arch", "manjaro"],
                    }
                    distros.append(distro)
                    print(f"[OK] {info['Name']}: {version}")
                else:
                    info = self.main_distros[project]
                    desc = self.descriptions.get(info["Name"], {"tr": info["Name"], "en": info["Name"]})
                    distros.append({
                        "id": project,
                        "name": info["Name"],
                        "description_tr": desc["tr"],
                        "description_en": desc["en"],
                        "category": info["Category"],
                        "website_url": info["Website"],
                        "download_url": info["Download"],
                        "version": "Güncel",
                        "hardware": self._get_hardware_req(info["Category"]),
                        "icon_text": self.icons.get(info["Name"], info["Name"][0]),
                        "best_of_year": project in ["linuxmint", "ubuntu", "fedora", "debian", "arch", "manjaro"],
                    })
                    
                if (i + 1) % 5 == 0:
                    time.sleep(1)
                    
            except Exception as e:
                print(f"[X] {project}: {str(e)[:30]}")
                continue
                    
        return distros

    def _get_latest_version(self, data):
        stable_versions = []
        
        for item in data:
            status = item.get("status", "").lower()
            version = item.get("version", "")
            
            if version:
                if "stable" in status or "newest" in status:
                    return version
                elif "unique" in status or "legacy" not in status:
                    stable_versions.append(version)
        
        if stable_versions:
            return stable_versions[0]
        
        if data:
            return data[0].get("version", "Güncel")
        return "Güncel"

    def _get_hardware_req(self, category):
        if category == "Hafif (Eski PC)":
            return "1GB RAM+"
        elif category == "Pentest (Güvenlik)":
            return "4GB RAM+"
        elif category == "Server":
            return "2GB RAM+"
        return "4GB RAM+"

    def scrape_all(self, limit=50):
        print("\n=== LinuXplore Repology API Güncelleme ===\n")
        distros = self.fetch_repology()
        
        if not distros:
            print("Repology'den veri çekilemedi, lokal veri kullanılıyor.")
            distros = self._get_fallback()
        
        distros.sort(key=lambda x: x["name"])
        
        self._save_to_json(distros)
        print(f"\n=== Tamamlandı! {len(distros)} dağıtım güncellendi ===\n")
        return distros

    def _get_fallback(self):
        distros = []
        for project, info in self.main_distros.items():
            desc = self.descriptions.get(info["Name"], {"tr": info["Name"], "en": info["Name"]})
            distros.append({
                "id": project,
                "name": info["Name"],
                "description_tr": desc["tr"],
                "description_en": desc["en"],
                "category": info["Category"],
                "website_url": info["Website"],
                "download_url": info["Download"],
                "version": "Güncel",
                "hardware": self._get_hardware_req(info["Category"]),
                "icon_text": self.icons.get(info["Name"], info["Name"][0]),
                "best_of_year": project in ["linuxmint", "ubuntu", "fedora", "debian", "arch", "manjaro"],
            })
        return distros

    def _save_to_json(self, data):
        os.makedirs("src/data", exist_ok=True)
        with open("src/data/distros.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def update_distros():
    scraper = DistroScraper()
    return scraper.scrape_all()

if __name__ == "__main__":
    update_distros()
