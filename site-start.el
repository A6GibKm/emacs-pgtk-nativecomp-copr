;; Aspell is a replacement for ispell
(setq-default ispell-program-name "aspell") 

;; Add python support
(require 'python-mode)
(setq auto-mode-alist
      (cons '("\\.py$" . python-mode) auto-mode-alist))
(setq interpreter-mode-alist
      (cons '("python" . python-mode) interpreter-mode-alist))

;; run functions from the /usr/share/emacs/site-lisp/site-start.d directory
;; Files in this directory ending with ".el" are run on startup

(mapc 'load (directory-files "/usr/share/emacs/site-lisp/site-start.d" t "\\.el\\'"))

;; Use the rpm-spec-mode for spec files
(require 'rpm-spec-mode)
(setq auto-mode-alist
      (cons '("\\.spec$" . rpm-spec-mode) auto-mode-alist))

;; Enable utf-8 in locales using utf-8. In RHL, all of these end in .UTF-8
;; The utf-8 support in emacs is limited, problems can be expected - especially
;; outside latin1

(cond ((equal (substring (concat "     " (getenv "LANG")) -5) "UTF-8")
      (setq locale-coding-system 'utf-8)
      (set-terminal-coding-system 'utf-8)
      (set-keyboard-coding-system 'utf-8)
      (set-selection-coding-system 'utf-8)
      (prefer-coding-system 'utf-8)))



