#!/bin/bash


# checks

## python
clear
echo "--> starting command tests"
if ! command -v python3 &> /dev/null
then
    echo "[HATA] python bulunamadı.. lütfen pythonu indirin."
    exit
else
    echo "[BAŞARILI] python bulundu | başlatılıyor..."
fi

## git

if ! command -v git &> /dev/null
then
    echo "[HATA] git bulunamadı... lütfen git'i indirin."
    exit
else
    echo "[BAŞARILI] git bulundu | başlatılıyor..."
fi

if ! command -v nano &> /dev/null; then
    echo "[HATA] nano bulunamadı... hesaplar.txt'i açarken hatalar olabilir."
else
    echo "[BAŞARILI] nano bulundu | başlatılıyor..."
fi


echo ""
echo ""


# Checks if MCsniperPY is already installed

if [ -d cenks sniper ]; then
    cd MCsniperPY
elif [[ "${PWD##*/}" == "cenks sniper" ]]; then
    echo "[BAŞARILI] sen zaten cenks sniper'ı indirmişsin."
    echo ""
    echo ""
else
    echo "[BAŞARILI] cenks sniper indiriliyor..."
    git clone -q https://github.com/cenkh/cenks-sniper
    echo "[BAŞARILI] cenks sniper indirildi"
    cd cenks sniper
    echo ""
    echo ""
fi


if [ ! -e already_setup ]
then
    echo "[BAŞARILI] gerekenler.txt indiriliyor..."
    python3 -m pip install -q -r gerekenler.txt
    echo "[BAŞARILI] gerekenler indirildi!"
    echo > already_setup
    echo ""
    echo ""
fi

changed=0
git remote update && git status -uno | grep -q '' && changed=1
if [ $changed = 1 ]; then
    echo "[UYARI]cenks sniperın güncellemesi var!"
    read -p "cenks sniperı güncellemek istiyor musun (y/n)? " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "[BAŞARILI] cenks sniper güncelleniyor..."
	git pull -q
	echo "[BAŞARILI] cenks sniper güncellendi..."

    else
	echo "[UYARI] cenks sniper güncellenmiyor."
    fi
else
    echo "[BAŞARILI] cenks sniper güncellendi!"
fi

echo ""
echo ""

if [ ! -f hesaplar.txt ]
then
    echo > hesaplar.txt
    echo "[UYARI] hesaplar.txt bulunamadı!"
    echo "[BAŞARILI] hesaplar.txt dosyası oluşturuldu!"
    echo ""
    real_path=$(realpath hesaplar.txt)
    config_path=$(realpath ayarlar.txt)
    echo "Lütfen hesaplarını hesaplar.txt'e gir."
    echo "Bu Şekilde gir email:şifre"
    read -p "hesaplar.txt'i açmak için herhangi bir tuşa bas... " -n 1 -r
    nano hesaplar.txt
    echo ""
    echo ""
    read -p "Devam etmek için herhangi bir tuşa Bas... " -n -1 -r
else
    echo "[BAŞARILI] hesaplar.txt zaten var."
fi

clear

python3 snipe.py
