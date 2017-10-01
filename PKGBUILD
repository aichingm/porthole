# Maintainer: Mario Aichinger <aichingm@gmail.com>
_pkgname=porthole
pkgname="${_pkgname}-git"
pkgver=20171001222649
pkgrel=1
pkgdesc="Porthole"
arch=('any')
url="https://github.com/aichingm/porthole"
license=('GPL3')
depends=('dmenu' 'python' 'python-pynput' 'python-pyqt5' 'qt5-webengine')
makedepends=('git')
provides=('porthole')
options=(!emptydirs)
source=("git+${url}")
md5sums=('SKIP')

pkgver() {
  cd "$srcdir/${_pkgname}"
  date --date="$(git log -1 --date=iso --format=%cd)" "+%Y%m%d%H%M%S"
}

package() {
  cd "$srcdir/${_pkgname}"
  python setup.py install --root="$pkgdir/" --optimize=1
  install -Dm755 "${srcdir}/${_pkgname}/porthole.desktop" "${pkgdir}/usr/share/applications/porthole.desktop"
  install -Dm755 "${srcdir}/${_pkgname}/Porthole/res/icon.png" "${pkgdir}/usr/share/pixmaps/porthole.png"
}

# vim:set ts=2 sw=2 et:
