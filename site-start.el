;; Aspell is a replacement for ispell
(setq-default ispell-program-name "aspell") 

;; Add python support
(setq auto-mode-alist
      (cons '("\\.py$" . python-mode) auto-mode-alist))
(setq interpreter-mode-alist
      (cons '("python" . python-mode)
            interpreter-mode-alist))
