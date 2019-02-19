pkgname=scrap-revuedepresse-git
pkgver=0.0.1
pkgrel=1
provides=("${pkgname%-git}")
conflicts=("${pkgname%-git}")
pkgdesc="Scrap the revuedepresse website"
arch=('any')
url="https://github.com/dbeley/${pkgname%-git}"
license=('MIT')
depends=(
    'python'
    'python-setuptools'
    'python-requests'
    'python-lxml'
    'python-beautifulsoup4'
    'python-urllib3'
    )
source=("git+https://github.com/dbeley/${pkgname%-git}")
md5sums=("SKIP")

package() {
  cd "${pkgname%-git}"
  python setup.py install --prefix=/usr --root="$pkgdir/" --optimize=1 --skip-build
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 "$srcdir/${pkgname%-git}/systemd-service/revuedepresse.service" "$pkgdir/usr/lib/systemd/system/revuedepresse.service"
  install -Dm644 "$srcdir/${pkgname%-git}/systemd-service/revuedepresse.timer" "$pkgdir/usr/lib/systemd/system/revuedepresse.timer"
  install -Dm644 "$srcdir/${pkgname%-git}/systemd-service/revuedepresse_simple.service" "$pkgdir/usr/lib/systemd/system/revuedepresse_simple.service"
  install -Dm644 "$srcdir/${pkgname%-git}/systemd-service/revuedepresse_simple.timer" "$pkgdir/usr/lib/systemd/system/revuedepresse_simple.timer"
}
