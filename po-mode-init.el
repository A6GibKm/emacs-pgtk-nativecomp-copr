;; Use po-mode for translation files

(autoload 'po-mode "po-mode")
(setq auto-mode-alist (cons '("\\.po[tx]?\\'\\|\\.po\\." . po-mode)
                            auto-mode-alist))

;;; To automatically use proper fonts under Emacs 20, also add:

(autoload 'po-find-file-coding-system "po-mode")
(modify-coding-system-alist 'file "\\.po[tx]?\\'\\|\\.po\\."
                            'po-find-file-coding-system)

