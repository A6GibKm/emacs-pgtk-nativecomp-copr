;; aspell is a replacement for ispell (this duplicates of aspell-init.el)
(setq-default ispell-program-name "aspell") 

;; load ".el" files in "/usr/share/emacs/site-lisp/site-start.d/" on startup
(mapc 'load
      (directory-files "/usr/share/emacs/site-lisp/site-start.d" t "\\.el\\'"))

;; Enable utf-8 in locales using utf-8. In RHL, all of these end in ".UTF-8".
;; The utf-8 support in Emacs is limited, problems can be expected - especially
;; outside latin-1
(cond ((equal (substring (concat "     " (or (getenv "LC_ALL")
					     (getenv "LC_CTYPE")
					     (getenv "LANG")))
			 -5)
	      "UTF-8")
       (setq locale-coding-system 'utf-8)
       (set-terminal-coding-system 'utf-8)
       (set-keyboard-coding-system 'utf-8)
       (set-selection-coding-system 'utf-8)
       (prefer-coding-system 'utf-8)))
