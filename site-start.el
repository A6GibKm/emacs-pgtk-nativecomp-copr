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
