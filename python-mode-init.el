;; setup python support

(autoload 'python-mode "python-mode" "Python mode." t)
(autoload 'py-shell "python-mode" "Python shell mode." t)
(add-to-list 'auto-mode-alist '("\\.py$" . python-mode))
(add-to-list 'interpreter-mode-alist '("python" . python-mode))
