;;; default.el - loaded after ".emacs" on startup
;;;
;;; Setting `inhibit-default-init' non-nil in "~/.emacs"
;;; prevents loading of this file.  Also the "-q" option to emacs
;;; prevents both "~/.emacs" and this file from being loaded at startup.

;; always end a file with a newline
(defvar require-final-newline 'query)

;; stop at the end of the file, not just add lines
(defvar next-line-add-newlines nil)

(when window-system
  ;; enable wheelmouse support by default
  (mwheel-install))
