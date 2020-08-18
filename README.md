[![Copr build status](https://copr.fedorainfracloud.org/coprs/deathwish/emacs-pgtk-nativecomp/package/emacs/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/deathwish/emacs-pgtk-nativecomp/package/emacs/)

## Pure Gtk and native compilation builds of GNU Emacs

- [masm11/emacs](https://github.com/masm11/emacs)
- [fejfighter/emacs](https://github.com/fejfighter/emacs)

This package is mostly aligned with the GNU Emacs package from
official Fedora repositories.
- [https://src.fedoraproject.org/rpms/emacs](https://src.fedoraproject.org/rpms/emacs)

## Changes in Emacs 28
- [`NEWS` file from `master`
  branch](https://git.savannah.gnu.org/cgit/emacs.git/tree/etc/NEWS?h=master)

## Credits & Licensing
The repository
[A6GibKm/emacs-pgtk-nativecomp-copr](https://github.com:A6GibKm/emacs-pgtk-nativecomp-copr)
containing build recipes for [Copr project
emacs-gtk-native-comp](https://copr.fedorainfracloud.org/coprs/deathwish/emacs-pgtk-nativecomp/)
is a fork of
[https://src.fedoraproject.org/rpms/emacs](https://src.fedoraproject.org/rpms/emacs).

This fork as well as the original repository ([according to
FPCA](https://fedoraproject.org/wiki/Legal:Fedora_Project_Contributor_Agreement#Other_FAQs))
are licensed under MIT License. See
[LICENSE](https://github.com/A6GibKm/emacs-pgtk-nativecomp-copr/blob/master/LICENSE)
for the full license text.

## How to install/update
- Enable this copr repository,
  ```sh
  $ dnf copr enable deathwish/emacs-pgtk-nativecomp
  ```
- Install latest pretest,
  ```sh
   $ dnf install emacs
  ```
  or update the installed version,
  ```sh
  $ dnf update emacs
  ```

## Reporting issues
If you face any issues while installing or updating, please create an
issue on [GitHub repository
here](https://github.com/A6GibKm/emacs-pgtk-nativecomp-copr).
