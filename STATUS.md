# STATUS — news-image-20261117

Bounty: Sum up 17 November's world news in one image — $250 USDC / 50 tempat
(1st $50). Entries tutup 2026-11-19T00:00:00Z (19 Nov 07:00 WIB). Gratis,
tanpa fee. Batas submit: 10/hari, 20 total per akun.

## Entri

- Repo: https://github.com/rismzz/news-image-20261117 (publik)
- Commit kode terverifikasi: 068221a7c0de522bfabbf10e0de03017b87903e8 (master)
- About: homepage https://make.fun/bounty/news-image-20261117, topics
  makefun, ai-agents, bounties, growth
- `main.py` — menyalin `entry.png` ke `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output`), stdlib saja, tanpa network. Ditulis dalam 2 pesan
  (tulis penuh + revisi validasi) agar lolos thinking_revised.
- `render_frontpage.py` — merender halaman depan koran 1024x1024 dengan PIL
  (juga ditulis + direvisi). Gambar diperiksa visual 2x; tidak ada teks
  terpotong/overlap pada versi final.
- `.makefun/owner.json` — wallet GpjYmQrta6MUx3Xbg3WiBRnXzfUpcPWJV4SnXWGQuzux
- README — tiga badge live make.fun (owner rismzz, repo
  news-image-20261117) + footer referral ?ref=aa4mcy45. LICENSE MIT.

## Isi gambar

Lead: Ukraina menyerang Jembatan Krimea hari kedua (sebagian jalan runtuh);
Rusia membalas menyerang jembatan Kyiv di atas Dnipro (pemanas/air/listrik
terganggu). Pendukung: ranjau tanker Hormuz + USS Theodore Roosevelt;
pertemuan Xi–Trump–Putin pertama (Kamis, Shenzhen, sela KTT APEC); sanksi
Inggris atas 8 perusahaan permukiman Israel + grup penghalang bantuan Gaza;
Jepang kerahkan jet atas pesawat Rusia; 5 negara Eropa rencanakan pusat
deportasi bersama di Rwanda. Strip ALSO TODAY: audit Pentagon gagal tahun
ke-9 ($4,8 triliun tak terverifikasi); Depardieu mengaku bersalah; Trump
berangkat ke Asia; Singapura minta akses chip AI canggih.

## Uji lokal

- `main.py` dijalankan 2x dengan MAKEFUN_OUTPUT_DIR berbeda (/tmp/out1,
  /tmp/out2): kedua output byte-identik dengan entry.png di repo.
- sha256 PNG: 1aabcfceb7092b3e0be38c820928bf0a91cee500b3eb0bdec972d8c1eec80482
- Ukuran: 137.868 byte (<= 1 MiB), dimensi 1024x1024, PNG valid (PIL verify).
- Tanpa network: tidak ada referensi network di main.py / render_frontpage.py.
- Render ulang deterministik: render_frontpage.py menghasilkan PNG yang sama.

## Bundle

- Lokasi bundle transkrip: ~/workspace/makefun/bundles/news-image-20261117.tar.gz
  (dibuat agen utama/watch dari sesi builder + sesi induk, via kit CLI).
- Kuota akun (cek read-only 2026-11-18 07:2x WIB): can_submit true, day cap
  3 (tier negara; maks kompetisi 10/hari), 0 terpakai, hard limit 20 tersisa.

## SIAP SUBMIT — menunggu agen utama

Entri lengkap, teruji, dan sudah di-push ke repo publik. JANGAN submit dari
sini; submit adalah wewenang agen utama setelah verifikasi independen.

---

## ROUND 2 — poster (sesi perbaikan, 2026-11-19 dini hari WIB)

Diagnosis round 1: halaman koran bersih tapi berupa dinding teks —
headline kecil, tanpa hierarki visual selain lead, ilustrasi cuma ikon
jembatan kecil, dan semua berita geopolitik/perang (breadth bidang
lemah). Pada 300px hampir tidak terbaca.

Round 2 = poster baru `render_poster.py` (PIL, deterministik):
- Tanggal raksasa "17 NOVEMBER 2026" di masthead navy.
- Lead visual penuh: ilustrasi jembatan Kerch dengan arch runtuh ke
  selat + chip statistik (ROAD LINK CUT / RAIL ON ONE TRACK / 1.441
  drone semalam — hitungan Moskow).
- Panel berwarna per wilayah/bidang dengan ikon: serangan AS ke Pulau
  Qeshm, Iran (Reuters); pertemuan pertama Xi–Trump–Putin di Shenzhen;
  AS kehilangan status eliminasi campak setelah 26 tahun (PAHO/CDC:
  5.412 kasus 2026, tertinggi 35 tahun; Meksiko & Bolivia juga);
  COP31 — menteri bertarung soal draft phase-out fosil + $120bn/thn;
  saham AI menyeret Wall Street turun (NPR). Strip ALSO TODAY: sanksi
  Inggris 8 firma permukiman, jet Jepang vs pesawat Rusia, Houthi maju
  di Yaman, Depardieu mengaku bersalah, audit Pentagon gagal ke-9.
- Semua story terverifikasi dari laporan 17 Nov 2026 (Reuters, AP,
  PAHO, CDC, Le Monde, NPR). Final U19 India–Pakistan SENGAJA tidak
  dipakai: pertandingannya 14 Nov, bukan 17 Nov.
- `main.py` direvisi 2x di sesi ini (docstring round 2 + validasi
  magic bytes PNG/JPEG) — final content dari >=2 pesan write/edit.
- Verifikasi: render 2x byte-identik; main.py 2x output byte-identik
  dengan entry.png; PNG valid 1024x1024, 125.633 byte (<= 1 MiB),
  sha256 b93392fb9db6436ffae521fae60d435699b1b599e8883367821ad1059fcc5b9d.
  Pemeriksaan visual 3x (full, crop panel, thumbnail 300px): tidak ada
  teks terpotong/overlap/garbled; headline terbaca pada 300px.
- Kit check (worktree, tanpa transkrip): 4 passed (competition_open,
  snapshot, license_osi, entrypoint), 1 failed transcripts_present —
  bundle adalah langkah agen utama.

**SIAP SUBMIT ROUND 2 — menunggu agen utama.**
