;; Use php-mode for .php,.php3,.php4 and .phtml files

(autoload 'php-mode "php-mode")
(setq auto-mode-alist (cons '("\\.php[34]\\|.php\\|.phtml" . php-mode)
                            auto-mode-alist))

