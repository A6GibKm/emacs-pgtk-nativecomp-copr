;;; rpm-spec-mode.el --- RPM spec file editing commands for Emacs/XEmacs

;; Copyright (C) 1997,1998,1999,2000,2001 Stig Bjørlykke, <stigb@tihlde.org>

;; Author:   Stig Bjørlykke, <stigb@tihlde.org>
;; Keywords: unix, languages
;; Version:  0.11e

;; This file is not yet part of FSF Emacs or XEmacs.

;; Emacs/XEmacs is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2, or (at your option)
;; any later version.

;; Emacs/XEmacs is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
;; General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with Emacs/XEmacs; see the file COPYING.  If not, write to the
;; Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
;; MA 02111-1307, USA.

;;; Synched up with:  both in FSF Emacs and XEmacs.

;;; Thanx to:

;;     Tore Olsen <toreo@tihlde.hist.no> for some general fixes. 
;;     Steve Sanbeg <sanbeg@dset.com> for navigation functions and
;;          some Emacs fixes.

;;; ToDo:

;; - rewrite function names and shortcuts.
;; - autofill changelog entries.
;; - customize rpm-tags-list and rpm-group-tags-list.
;; - get values from `rpm --showrc'.
;; - ssh/rsh for compile.
;; - finish integrating the new navigation functions in with existing stuff. 
;; - use a single prefix conistently (internal)

;;; Commentary:

;; This mode is used for editing spec files used for building RPM packages.
;;
;; Most recent version is available from:
;;  <URL:http://www.tihlde.org/~stigb/rpm-spec-mode.el>
;;
;; Put this in your .emacs file to enable autoloading of rpm-spec-mode,
;; and auto-recognition of ".spec" files:
;;
;;  (autoload 'rpm-spec-mode "rpm-spec-mode.el" "RPM spec mode." t)
;;  (setq auto-mode-alist (append '(("\\.spec" . rpm-spec-mode))
;;                                auto-mode-alist))
;;------------------------------------------------------------
;;
;; Adapted for Red Hat and some fixes made by Tim Powers <timp@redhat.com>
;; and Trond Eivind Glomsrød <teg@redhat.com>.
;;
;; Adapted by Chmouel Boudjnah <chmouel@mandrakesoft.com> for Mandrake

;;; Code:

(defgroup rpm-spec nil
  "RPM Spec mode with Emacs/XEmacs enhancements."
  :prefix "rpm-spec"
  :group 'languages)

(defcustom rpm-spec-add-attr nil
  "Add %attr entry for filelistings or not."
  :type 'boolean
  :group 'rpm-spec)

(defcustom rpm-spec-short-circuit nil
  "Skip straight to specified stage.
(ie, skip all stages leading up to the specified stage).  Only valid
in \"%build\" and \"%install\" stage."
  :type 'boolean
  :group 'rpm-spec)

(defcustom rpm-spec-timecheck "0"
  "Set the \"timecheck\" age (0 to disable).
The timecheck value expresses, in seconds, the maximum age of a file
being packaged.  Warnings will be printed for all files beyond the
timecheck age."
  :type 'integer
  :group 'rpm-spec)

(defcustom rpm-spec-buildroot ""
  "Override the BuildRoot tag with directory <dir>."
  :type 'string
  :group 'rpm-spec)

(defcustom rpm-spec-target ""
  "Interpret given string as `arch-vendor-os'.
Set the macros _target, _target_arch and _target_os accordingly"
  :type 'string
  :group 'rpm-spec)

(defcustom rpm-spec-clean nil
  "Remove the build tree after the packages are made."
  :type 'boolean
  :group 'rpm-spec)

(defcustom rpm-spec-rmsource nil
  "Remove the source and spec file after the packages are made."
  :type 'boolean
  :group 'rpm-spec)

(defcustom rpm-spec-test nil
  "Do not execute any build stages.  Useful for testing out spec files."
  :type 'boolean
  :group 'rpm-spec)

(defcustom rpm-spec-sign-gpg nil
  "Embed a GPG signature in the package.
This signature can be used to verify the integrity and the origin of
the package."
  :type 'boolean
  :group 'rpm-spec)

(defcustom rpm-initialize-sections t
  "Automatically add empty section headings to new spec files."
  :type 'boolean
  :group 'rpm-spec)

(defcustom rpm-insert-version t
  "Automatically add version in a new changelog entry."
  :type 'boolean
  :group 'rpm-spec)

(defgroup rpm-spec-faces nil
  "Font lock faces for RPM Spec mode."
  :group 'rpm-spec
  :group 'faces)

;;------------------------------------------------------------
;; variables used by navigation functions.

(defconst rpm-sections 
  '("preamble" "description" "prep" "setup" "build" "install" "clean"
    "changelog" "files")
  "Partial list of section names.")
(defvar rpm-section-list
  '(("preamble") ("description") ("prep") ("setup") ("build") ("install")
	 ("clean") ("changelog") ("files"))
  "Partial list of section names.")
(defconst rpm-scripts 
  '("pre" "post" "preun" "postun" "trigger" "triggerun" "triggerpostun")
  "List of rpm scripts")
(defconst rpm-section-seperate "^%\\(\\w+\\)\\s-")
(defconst rpm-section-regexp 
  "^%\\(\\(description\\)\\|\\(prep\\)\\|\\(changelog\\)\\|\\(build\\)\\|\\(install\\)\\|\\(files\\)\\|\\(clean\\)\\|\\(package\\)\\|\\(pre\\|post\\(un\\)?\\)\\|\\(trigger\\(post\\)?\\([iu]n\\)?\\)\\)\\b"
  "Regular expression to match beginning of a section.")

;;------------------------------------------------------------

(defface rpm-spec-tag-face
    '(( ((class color) (background light)) (:foreground "blue") )
      ( ((class color) (background dark)) (:foreground "blue") ))
  "*The face used for tags."
  :group 'rpm-spec-faces)

(defface rpm-spec-macro-face
    '(( ((class color) (background light)) (:foreground "purple") )
      ( ((class color) (background dark)) (:foreground "yellow") ))
  "*The face used for macros."
  :group 'rpm-spec-faces)

(defface rpm-spec-doc-face
    '(( ((class color) (background light)) (:foreground "magenta") )
      ( ((class color) (background dark)) (:foreground "magenta") ))
  "*The face used for document files."
  :group 'rpm-spec-faces)

(defface rpm-spec-dir-face
    '(( ((class color) (background light)) (:foreground "green") )
      ( ((class color) (background dark)) (:foreground "green") ))
  "*The face used for directories."
  :group 'rpm-spec-faces)

(defface rpm-spec-package-face
    '(( ((class color) (background light)) (:foreground "red") )
      ( ((class color) (background dark)) (:foreground "red") ))
  "*The face used for files."
  :group 'rpm-spec-faces)

(defface rpm-spec-ghost-face
    '(( ((class color) (background light)) (:foreground "red") )
      ( ((class color) (background dark)) (:foreground "red") ))
  "*The face used for ghost tags."
  :group 'rpm-spec-faces)

;;; GNU emacs font-lock needs these...
(defvar rpm-spec-macro-face 'rpm-spec-macro-face "*Face for macros")
(defvar rpm-spec-tag-face 'rpm-spec-tag-face "*Face for tags")
(defvar rpm-spec-package-face 'rpm-spec-package-face "*Face for package tag")
(defvar rpm-spec-dir-face 'rpm-spec-dir-face "*Face for directory entries")
(defvar rpm-spec-doc-face 'rpm-spec-doc-face "*Face for documentation entries")
(defvar rpm-spec-ghost-face 'rpm-spec-ghost-face "*Face for %ghost files")

(defvar rpm-default-umask "-"
  "*Default umask for files, specified with %attr")
(defvar rpm-default-owner "root" 
  "*Default owner for files, specified with %attr")
(defvar rpm-default-group "root" 
  "*Default group for files, specified with %attr")

;;------------------------------------------------------------

(defvar rpm-no-gpg nil "Tell rpm not to sign package.")

(defvar rpm-tags-list
  '(("Autoreqprov")
    ("Buildroot")
    ("Conflicts")
    ("Copyright")
    ("%description")
    ("Distribution")
    ("Excludearch")
    ("Excludeos")
    ("Exclusivearch")
    ("Exclusiveos")
    ("%files")
    ("Group")
    ("Icon")
    ("%ifarch")
    ("Name")
    ("Nopatch")
    ("Nosource")
    ("%package")
    ("Packager")
    ("Patch")
    ("Prefix")
    ("Provides")
    ("Release")
    ("Requires")
    ("Serial")
    ("Source")
    ("Summary")
    ("Url")
    ("Vendor")
    ("Version"))
  "List which elements are valid tags.")

(defvar rpm-group-tags-list
  '(("Amusements/Games")
    ("Amusements/Graphics")
    ("Applications/Archiving")
    ("Applications/Communications")
    ("Applications/Databases")
    ("Applications/Editors")
    ("Applications/Emulators")
    ("Applications/Engineering")
    ("Applications/File")
    ("Applications/Internet")
    ("Applications/Multimedia")
    ("Applications/Productivity")
    ("Applications/Publishing")
    ("Applications/System")
    ("Applications/Text")
    ("Development/Debuggers")
    ("Development/Languages")
    ("Development/Libraries")
    ("Development/System")
    ("Development/Tools")
    ("Documentation")
    ("System Environment/Base")
    ("System Environment/Daemons")
    ("System Environment/Kernel")
    ("System Environment/Libraries")
    ("System Environment/Shells")
    ("User Interface/Desktops")
    ("User Interface/X")
    ("User Interface/X Hardware Support")
    )
  "List which elements is valid group tags.")

(defvar rpm-spec-mode-syntax-table nil
  "Syntax table in use in RPM-Spec-mode buffers.")
(unless rpm-spec-mode-syntax-table
  (setq rpm-spec-mode-syntax-table (make-syntax-table))
  (modify-syntax-entry ?\\ "\\" rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?\n ">   " rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?\f ">   " rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?\# "<   " rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?/ "." rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?* "." rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?+ "." rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?- "." rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?= "." rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?% "_" rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?< "." rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?> "." rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?& "." rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?| "." rpm-spec-mode-syntax-table)
  (modify-syntax-entry ?\' "." rpm-spec-mode-syntax-table))

(defvar rpm-spec-mode-map nil
  "Keymap used in RPM Spec mode.")
(unless rpm-spec-mode-map
  (setq rpm-spec-mode-map (make-sparse-keymap))
  (and (functionp 'set-keymap-name)
       (set-keymap-name rpm-spec-mode-map 'rpm-spec-mode-map))
  (define-key rpm-spec-mode-map "\C-ca" 'rpm-build-ba)
  (define-key rpm-spec-mode-map "\C-cb" 'rpm-build-bb)
  (define-key rpm-spec-mode-map "\C-cc" 'rpm-build-bc)
  (define-key rpm-spec-mode-map "\C-ce" 'rpm-add-change-log-entry)
  (define-key rpm-spec-mode-map "\C-cg" 'rpm-goto-section)
  (define-key rpm-spec-mode-map "\C-ci" 'rpm-build-bi)
  (define-key rpm-spec-mode-map "\C-cl" 'rpm-build-bl)
  (define-key rpm-spec-mode-map "\C-cp" 'rpm-build-bp)
  (define-key rpm-spec-mode-map "\C-cr" 'rpm-increase-release-tag)
  (define-key rpm-spec-mode-map "\C-cs" 'rpm-build-bs)
  (define-key rpm-spec-mode-map "\C-cxa" 'rpm-toggle-add-attr)
  (define-key rpm-spec-mode-map "\C-cxb" 'rpm-change-buildroot-option)
  (define-key rpm-spec-mode-map "\C-cxc" 'rpm-toggle-clean)
  (define-key rpm-spec-mode-map "\C-cxg" 'rpm-toggle-sign-gpg)
  (define-key rpm-spec-mode-map "\C-cxi" 'rpm-change-timecheck-option)
  (define-key rpm-spec-mode-map "\C-cxp" 'rpm-change-target-option)
  (define-key rpm-spec-mode-map "\C-cxr" 'rpm-toggle-rmsource)
  (define-key rpm-spec-mode-map "\C-cxs" 'rpm-toggle-short-circuit)
  (define-key rpm-spec-mode-map "\C-cxt" 'rpm-toggle-test)
  ;;May be better to have movement commands on \C-ck, and build on \C-c\C-k
  (define-key rpm-spec-mode-map "\C-c\C-i" 'rpm-insert-tag)
  (define-key rpm-spec-mode-map "\C-u\C-c\C-i" 'rpm-change-tag)
  (define-key rpm-spec-mode-map "\C-c\C-n" 'rpm-forward-section)
  (define-key rpm-spec-mode-map "\C-c\C-p" 'rpm-backward-section)
  (define-key rpm-spec-mode-map "\C-c\C-t" 'rpm-insert-true-prefix)
  (define-key rpm-spec-mode-map "\C-c\C-cg" 'rpm-files-group)
  (define-key rpm-spec-mode-map "\C-c\C-co" 'rpm-files-owner)
  (define-key rpm-spec-mode-map "\C-c\C-cu" 'rpm-files-umask)
  (define-key rpm-spec-mode-map "\C-c\C-dd" 'rpm-insert-dir)
  (define-key rpm-spec-mode-map "\C-c\C-do" 'rpm-insert-docdir)
  (define-key rpm-spec-mode-map "\C-c\C-fc" 'rpm-insert-config)
  (define-key rpm-spec-mode-map "\C-c\C-fd" 'rpm-insert-doc)
  (define-key rpm-spec-mode-map "\C-c\C-ff" 'rpm-insert-file)
  (define-key rpm-spec-mode-map "\C-c\C-fg" 'rpm-insert-ghost)
  ;(define-key rpm-spec-mode-map "\C-q" 'indent-spec-exp)
  ;(define-key rpm-spec-mode-map "\t" 'sh-indent-line)
  )

(defconst rpm-spec-mode-menu
  (purecopy '("RPM-Spec"
         ["Insert Tag"              rpm-insert-tag                t]
         ["Change Tag"              rpm-change-tag                t]
         "---"
         ["Go to section..."        rpm-mouse-goto-section  :keys "C-c g"]
         ["Forward section"         rpm-forward-section           t]
         ["Backward sectoin"        rpm-backward-section          t]
         "---"
         ["Add changelog entry..."  rpm-add-change-log-entry      t]
         ["Increase release-tag"    rpm-increase-release-tag      t]
         "---"
         ("Add file entry"
          ["Regular file..."        rpm-insert-file               t]
          ["Config file..."         rpm-insert-config             t]
          ["Document file..."       rpm-insert-doc                t]
          ["Ghost file..."          rpm-insert-ghost              t]
          "---"
          ["Directory..."           rpm-insert-dir                t]
          ["Document directory..."  rpm-insert-docdir             t]
          "---"
			 ["Insert %{prefix}"       rpm-insert-true-prefix        t] 
			 "---"
          ["Default add \"%attr\" entry" rpm-toggle-add-attr
           :style toggle :selected rpm-spec-add-attr]
          ["Change default umask for files..."  rpm-files-umask   t]
          ["Change default owner for files..."  rpm-files-owner   t]
          ["Change default group for files..."  rpm-files-group   t])
         ("Build Options"
          ["Short Circuit" rpm-toggle-short-circuit
           :style toggle :selected rpm-spec-short-circuit]
          ["Remove source" rpm-toggle-rmsource
           :style toggle :selected rpm-spec-rmsource]
          ["Clean"         rpm-toggle-clean
           :style toggle :selected rpm-spec-clean]
          ["Testing only"  rpm-toggle-test
           :style toggle :selected rpm-spec-test]
          ["GPG Sign"      rpm-toggle-sign-gpg
           :style toggle :selected rpm-spec-sign-gpg]
          "---"
          ["Change timecheck value..."  rpm-change-timecheck-option   t]
          ["Change buildroot value..."  rpm-change-buildroot-option   t]
          ["Change target value..."     rpm-change-target-option      t])
         ("RPM Build"
          ["Execute \"%prep\" stage"    rpm-build-bp                  t]
          ["Do a \"list check\""        rpm-build-bl                  t]
          ["Do the \"%build\" stage"    rpm-build-bc                  t]
          ["Do the \"%install\" stage"  rpm-build-bi                  t]
          "---"
          ["Build binary package"       rpm-build-bb                  t]
          ["Build source package"       rpm-build-bs                  t]
          ["Build binary and source"    rpm-build-ba                  t])
         "---"
         ["About rpm-spec-mode"         rpm-about-rpm-spec-mode       t]
         )))

(defvar rpm-spec-font-lock-keywords
  '(
    ("%[a-zA-Z0-9_]+" 0 rpm-spec-macro-face)
    ("^\\([a-zA-Z0-9]+\\)\\(\([a-zA-Z0-9]+\)\\):"
     (1 rpm-spec-tag-face)
     (2 rpm-spec-ghost-face))
    ("^\\([a-zA-Z0-9]+\\):" 1 rpm-spec-tag-face)
    ("%\\(define\\|files\\|package\\|description\\)[ \t]+\\([^ \t\n-]+\\)"
     (2 rpm-spec-package-face))
    ("%configure " 0 rpm-spec-macro-face)
    ("%dir[ \t]+\\([^ \t\n]+\\)[ \t]*" 1 rpm-spec-dir-face)
    ("%doc\\(\\|dir\\)[ \t]+\\(.*\\)\n" 2 rpm-spec-doc-face)
    ("%\\(ghost\\|config\\)[ \t]+\\(.*\\)\n" 2 rpm-spec-ghost-face)
    ("^%.+-[a-zA-Z][ \t]+\\([a-zA-Z0-9\.-]+\\)" 1 rpm-spec-doc-face)
    ("^\\(.+\\)(\\([a-zA-Z]\\{2,2\\}\\)):" 
     (1 rpm-spec-tag-face)
     (2 rpm-spec-doc-face))
    ("^\\*\\(.*[0-9] \\)\\(.*\\)\\(<.*>\\)\\(.*\\)\n"
     (1 rpm-spec-dir-face)
     (2 rpm-spec-package-face)
     (3 rpm-spec-tag-face)
     (4 font-lock-warning-face))
    ("%{[^{}]*}" 0 rpm-spec-macro-face)
    )
  "Additional expressions to highlight in RPM Spec mode.")

;;Initialize font lock for xemacs
(put 'rpm-spec-mode 'font-lock-defaults '(rpm-spec-font-lock-keywords))

(defvar rpm-spec-mode-abbrev-table nil
  "Abbrev table in use in RPM-Spec-mode buffers.")
(define-abbrev-table 'rpm-spec-mode-abbrev-table ())

;;------------------------------------------------------------

;;;###autoload
(defun rpm-spec-mode ()
  "Major mode for editing spec files.
This is much like C mode except for the syntax of comments.  It uses
the same keymap as C mode and has the same variables for customizing
indentation.  It has its own abbrev table and its own syntax table.

Turning on RPM Spec mode calls the value of the variable `rpm-spec-mode-hook'
with no args, if that value is non-nil."
  (interactive)
  (kill-all-local-variables)
  (condition-case nil
      (require 'shindent)
    (error
     (require 'sh-script)))
  (require 'cc-mode)
  (use-local-map rpm-spec-mode-map)
  (setq major-mode 'rpm-spec-mode)
  (setq mode-name "RPM-SPEC")
  (setq local-abbrev-table rpm-spec-mode-abbrev-table)
  (set-syntax-table rpm-spec-mode-syntax-table)

  (require 'easymenu)
  (easy-menu-define rpm-spec-call-menu rpm-spec-mode-map 
                    "Post menu for rpm-spec-mode" rpm-spec-mode-menu)
  (easy-menu-add rpm-spec-mode-menu)

  (if (= (buffer-size) 0)
      (rpm-spec-initialize))

  (make-local-variable 'paragraph-start)
  (setq paragraph-start (concat "$\\|" page-delimiter))
  (make-local-variable 'paragraph-separate)
  (setq paragraph-separate paragraph-start)
  (make-local-variable 'paragraph-ignore-fill-prefix)
  (setq paragraph-ignore-fill-prefix t)
;  (make-local-variable 'indent-line-function)
;  (setq indent-line-function 'c-indent-line)
  (make-local-variable 'require-final-newline)
  (setq require-final-newline t)
  (make-local-variable 'comment-start)
  (setq comment-start "# ")
  (make-local-variable 'comment-end)
  (setq comment-end "")
  (make-local-variable 'comment-column)
  (setq comment-column 32)
  (make-local-variable 'comment-start-skip)
  (setq comment-start-skip "#+ *")
;  (make-local-variable 'comment-indent-function)
;  (setq comment-indent-function 'c-comment-indent)
  ;;Initialize font lock for GNU emacs.
  (make-local-variable 'font-lock-defaults)
  (setq font-lock-defaults '(rpm-spec-font-lock-keywords nil t))
  (run-hooks 'rpm-spec-mode-hook))

(defun rpm-command-filter (process string)
  "Filter to process normal output."
  (save-excursion
    (set-buffer (process-buffer process))
    (save-excursion
      (goto-char (process-mark process))
      (insert-before-markers string)
      (set-marker (process-mark process) (point)))))

;;------------------------------------------------------------

(defun rpm-add-change-log-entry (&optional change-log-entry)
  "Find change log and add an entry for today."
  (interactive "sChangelog entry: ")
  (save-excursion
    (rpm-goto-section "changelog")
    (let ((string (concat "* " (substring (current-time-string) 0 11)
           (substring (current-time-string) -4) " "
           (user-full-name) " <" user-mail-address ">")))
      (if (not (search-forward string nil t))
     (insert "\n" string "\n")
   (forward-line 2))
      (insert "- " change-log-entry "\n"))))

;;------------------------------------------------------------

(defun rpm-insert-f (&optional filetype filename)
  "Insert new %files entry."
  (save-excursion
    (and (rpm-goto-section "files") (rpm-end-of-section))
    (if (or (eq filename 1) (not filename))
        (insert (read-file-name
                 (concat filetype "filename: ") "" "" nil) "\n")
      (insert filename "\n"))
    (forward-line -1)
    (if rpm-spec-add-attr
        (let ((rpm-default-mode rpm-default-umask))
          (insert "%attr(" rpm-default-mode ", " rpm-default-owner ", "
                  rpm-default-group ") ")))
    (insert filetype)))

(defun rpm-insert-file (&optional filename)
  "Insert regular file."
  (interactive "p")
  (rpm-insert-f "" filename))
  
(defun rpm-insert-config (&optional filename)
  "Insert config file."
  (interactive "p")
  (rpm-insert-f "%config " filename))

(defun rpm-insert-doc (&optional filename)
  "Insert doc file."
  (interactive "p")
  (rpm-insert-f "%doc " filename))

(defun rpm-insert-ghost (&optional filename)
  "Insert ghost file."
  (interactive "p")
  (rpm-insert-f "%ghost " filename))

(defun rpm-insert-dir (&optional dirname)
  "Insert directory."
  (interactive "p")
  (rpm-insert-f "%dir " dirname))

(defun rpm-insert-docdir (&optional dirname)
  "Insert doc directory."
  (interactive "p")
  (rpm-insert-f "%docdir " dirname))

;;------------------------------------------------------------

(defun rpm-insert (&optional what file-completion)
  "Insert given tag.  Use file-completion if argument is t."
  (beginning-of-line)
  (if (not what)
      (setq what (completing-read "Tag: " rpm-tags-list)))
  (if (string-match "^%" what)
      (setq read-text (concat "Packagename for " what ": ")
            insert-text (concat what " "))
    (setq read-text (concat what ": ")
          insert-text (concat what ": ")))
  (cond
   ((string-equal what "Group")
    (rpm-insert-group))
   ((string-equal what "Source")
    (rpm-insert-n "Source"))
   ((string-equal what "Patch")
    (rpm-insert-n "Patch"))
   (t
    (if file-completion
        (insert insert-text (read-file-name (concat read-text) "" "" nil) "\n")
      (insert insert-text (read-from-minibuffer (concat read-text)) "\n")))))

(defun rpm-topdir ()
  (or
   (getenv "RPM")
   (getenv "rpm")
   (if (file-directory-p "~/rpm") "~/rpm/")
   (if (file-directory-p "~/RPM") "~/RPM/")
   (if (file-directory-p "/usr/src/redhat/")"/usr/src/redhat/")
   "/usr/src/RPM"))

(defun rpm-insert-n (what &optional arg)
  "Insert given tag with possible number."
  (save-excursion
    (goto-char (point-max))
    (if (search-backward-regexp (concat "^" what "\\([0-9]*\\):") nil t)
        (let ((release (1+ (string-to-int (match-string 1)))))
          (forward-line 1)
          (let ((default-directory (concat (rpm-topdir) "/SOURCES/")))
            (insert what (int-to-string release) ": "
                    (read-file-name (concat what "file: ") "" "" nil) "\n")))
      (goto-char (point-min))
      (rpm-end-of-section)
      (insert what ": " (read-from-minibuffer (concat what "file: ")) "\n"))))

(defun rpm-change (&optional what arg)
  "Update given tag."
  (save-excursion
    (if (not what)
        (setq what (completing-read "Tag: " rpm-tags-list)))
    (cond
     ((string-equal what "Group")
      (rpm-change-group))
     ((string-equal what "Source")
      (rpm-change-n "Source"))
     ((string-equal what "Patch")
      (rpm-change-n "Patch"))
     (t
      (goto-char (point-min))
      (if (search-forward-regexp (concat "^" what ":\\s-*\\(.*\\)$") nil t)
          (replace-match
           (concat what ": " (read-from-minibuffer
                              (concat "New " what ": ") (match-string 1))))
        (message (concat what " tag not found...")))))))

(defun rpm-change-n (what &optional arg)
  "Change given tag with possible number."
  (save-excursion
    (goto-char (point-min))
    (let ((number (read-from-minibuffer (concat what " number: "))))
      (if (search-forward-regexp
           (concat "^" what number ":\\s-*\\(.*\\)") nil t)
          (let ((default-directory (concat (rpm-topdir) "/SOURCES/")))
            (replace-match
             (concat what number ": "
                     (read-file-name (concat "New " what number " file: ")
                                     "" "" nil (match-string 1)))))
        (message (concat what " number \"" number "\" not found..."))))))

(defun rpm-insert-group (group)
  "Insert Group tag."
  (interactive (list (completing-read "Group: " rpm-group-tags-list)))
  (beginning-of-line)
  (insert "Group: " group "\n"))

(defun rpm-change-group (&optional arg)
  "Update Group tag."
  (interactive "p")
  (save-excursion
    (goto-char (point-min))
    (if (search-forward-regexp "^Group: \\(.*\\)$" nil t)
        (replace-match
         (concat "Group: "
                 (insert (completing-read "Group: " rpm-group-tags-list
                                          nil nil (match-string 1)))))
      (message "Group tag not found..."))))

(defun rpm-insert-tag (&optional arg)
  "Insert a tag."
  (interactive "p")
  (rpm-insert))

(defun rpm-change-tag (&optional arg)
  "Change a tag."
  (interactive "p")
  (rpm-change))

(defun rpm-insert-packager (&optional arg)
  "Insert Packager tag."
  (interactive "p")
  (beginning-of-line)
  (insert "Packager: " (user-full-name) " <" user-mail-address ">\n"))

(defun rpm-change-packager (&optional arg)
  "Update Packager tag."
  (interactive "p")
  (rpm-change "Packager"))

;;------------------------------------------------------------

(defun rpm-current-section nil
  (interactive)
  (save-excursion
    (rpm-forward-section)
    (rpm-backward-section)
    (if (bobp) "preamble" 
      (buffer-substring (match-beginning 1) (match-end 1)))))

(defun rpm-backward-section nil
  "Move backward to the beginning of the previous section.
Go to beginning of previous section."
  (interactive)
  (or (re-search-backward rpm-section-regexp nil t)
      (goto-char (point-min))))

(defun rpm-beginning-of-section nil
  "Move backward to the beginning of the current section.
Go to beginning of current section."
  (interactive)
  (or (and (looking-at rpm-section-regexp) (point))
      (re-search-backward rpm-section-regexp nil t)
      (goto-char (point-min))))

(defun rpm-forward-section nil
  "Move forward to the beginning of the next section."
  (interactive)
  (forward-char)
  (if (re-search-forward rpm-section-regexp nil t)
      (progn (forward-line 0) (point))
    (goto-char (point-max))))

(defun rpm-end-of-section nil
  "Move forward to the end of this section."
  (interactive)
  (forward-char)
  (if (re-search-forward rpm-section-regexp nil t)
      (forward-line -1)
    (goto-char (point-max)))
;;  (while (or (looking-at paragraph-separate) (looking-at "^\\s-*#"))
  (while (looking-at "^\\s-*\\($\\|#\\)")
    (forward-line -1))
  (forward-line 1)
  (point))

(defun rpm-goto-section (section)
  "Move point to the beginning of the specified section; 
leave point at previous location."
  (interactive (list (completing-read "Section: " rpm-section-list)))
  (push-mark)
  (goto-char (point-min))
  (or 
   (equal section "preamble")
   (re-search-forward (concat "^%" section "\\b") nil t)
   (let ((s (cdr rpm-sections)))
     (while (not (equal section (car s)))
       (re-search-forward (concat "^%" (car s) "\\b") nil t)
       (setq s (cdr s)))
     (if (re-search-forward rpm-section-regexp nil t)
         (forward-line -1) (goto-char (point-max)))
     (insert "\n%" section "\n"))))

(defun rpm-mouse-goto-section (&optional section)
  (interactive 
   (x-popup-menu nil
    (list "sections" 
          (cons "Sections" (mapcar (lambda (e) (list e e)) rpm-sections))
          (cons "Scripts" (mapcar (lambda (e) (list e e)) rpm-scripts))
          )))
  (and section ;if user doesn't pick a section, exit quietly.
       (if (member section rpm-sections)
           (rpm-goto-section section)
         (goto-char (point-min))
         (or (re-search-forward (concat "^%" section "\\b") nil t)
             (and (re-search-forward "^%files\\b" nil t) (forward-line -1))
             (goto-char (point-max))))))

(defun rpm-insert-true-prefix () 
  (interactive)
  (insert "%{prefix}"))


;;------------------------------------------------------------

(defun rpm-build (buildoptions)
  "Build this rpm-package."
  (setq rpm-buffer-name
        (concat "*rpm " buildoptions " "
                (file-name-nondirectory buffer-file-name) "*"))
  (rpm-process-check rpm-buffer-name)
  (if (get-buffer rpm-buffer-name)
      (kill-buffer rpm-buffer-name))
  (create-file-buffer rpm-buffer-name)
  (display-buffer rpm-buffer-name)
  (setq buildoptions (list buildoptions buffer-file-name))
  (if (or rpm-spec-short-circuit rpm-spec-test)
      (setq rpm-no-gpg t))
  (if rpm-spec-rmsource
      (setq buildoptions (cons "--rmsource" buildoptions)))
  (if rpm-spec-clean
      (setq buildoptions (cons "--clean" buildoptions)))
  (if rpm-spec-short-circuit
      (setq buildoptions (cons "--short-circuit" buildoptions)))
  (if (and (not (equal rpm-spec-timecheck "0"))
           (not (equal rpm-spec-timecheck "")))
      (setq buildoptions (cons "--timecheck" (cons rpm-spec-timecheck
                                                   buildoptions))))
  (if (not (equal rpm-spec-buildroot ""))
      (setq buildoptions (cons "--buildroot" (cons rpm-spec-buildroot
                                                   buildoptions))))
  (if (not (equal rpm-spec-target ""))
      (setq buildoptions (cons "--target" (cons rpm-spec-target
                                                buildoptions))))
  (if rpm-spec-test
      (setq buildoptions (cons "--test" buildoptions)))
  (if (and rpm-spec-sign-gpg (not rpm-no-gpg))
      (setq buildoptions (cons "--sign" buildoptions)))
  (save-excursion
    (set-buffer (get-buffer rpm-buffer-name))
    (goto-char (point-max)))
  (let ((process
         (apply 'start-process "rpm" rpm-buffer-name "rpm" buildoptions)))
    (if (and rpm-spec-sign-gpg (not rpm-no-gpg))
        (let ((rpm-passwd-cache (read-passwd "GPG passphrase: ")))
          (process-send-string process (concat rpm-passwd-cache "\n"))))
    (set-process-filter process 'rpm-command-filter)))

(defun rpm-build-bp (&optional arg)
  "Run a `rpm -bp'."
  (interactive "p")
  (if rpm-spec-short-circuit
      (message "Cannot run `rpm -bp' with --short-circuit")
    (setq rpm-no-gpg t)
    (rpm-build "-bp")))

(defun rpm-build-bl (&optional arg)
  "Run a `rpm -bl'."
  (interactive "p")
  (if rpm-spec-short-circuit
      (message "Cannot run `rpm -bl' with --short-circuit")
    (setq rpm-no-gpg t)
    (rpm-build "-bl")))

(defun rpm-build-bc (&optional arg)
  "Run a `rpm -bc'."
  (interactive "p")
  (setq rpm-no-gpg t)
  (rpm-build "-bc"))

(defun rpm-build-bi (&optional arg)
  "Run a `rpm -bi'."
  (interactive "p")
  (setq rpm-no-gpg t)
  (rpm-build "-bi"))

(defun rpm-build-bb (&optional arg)
  "Run a `rpm -bb'."
  (interactive "p")
  (if rpm-spec-short-circuit
      (message "Cannot run `rpm -bb' with --short-circuit")
    (setq rpm-no-gpg nil)
    (rpm-build "-bb")))

(defun rpm-build-bs (&optional arg)
  "Run a `rpm -bs'."
  (interactive "p")
  (if rpm-spec-short-circuit
      (message "Cannot run `rpm -bs' with --short-circuit")
    (setq rpm-no-gpg nil)
    (rpm-build "-bs")))

(defun rpm-build-ba (&optional arg)
  "Run a `rpm -ba'."
  (interactive "p")
  (if rpm-spec-short-circuit
      (message "Cannot run `rpm -ba' with --short-circuit")
    (setq rpm-no-gpg nil)
    (rpm-build "-ba")))

(defun rpm-process-check (buffer)
  "Check if BUFFER has a running process.
If so, give the user the choice of aborting the process or the current
command."
  (let ((process (get-buffer-process (get-buffer buffer))))
    (if (and process (eq (process-status process) 'run))
        (if (yes-or-no-p (concat "Process `" (process-name process)
                                 "' running.  Kill it? "))
            (delete-process process)
          (error "Cannot run two simultaneous processes ...")))))

;;------------------------------------------------------------

(defun rpm-toggle-short-circuit (&optional arg)
  "Toggle rpm-spec-short-circuit."
  (interactive "p")
  (setq rpm-spec-short-circuit (not rpm-spec-short-circuit))
  (rpm-update-mode-name)
  (message (concat "Turned `--short-circuit' "
                   (if rpm-spec-short-circuit "on" "off") ".")))

(defun rpm-toggle-rmsource (&optional arg)
  "Toggle rpm-spec-rmsource."
  (interactive "p")
  (setq rpm-spec-rmsource (not rpm-spec-rmsource))
  (rpm-update-mode-name)
  (message (concat "Turned `--rmsource' "
                   (if rpm-spec-rmsource "on" "off") ".")))

(defun rpm-toggle-clean (&optional arg)
  "Toggle rpm-spec-clean."
  (interactive "p")
  (setq rpm-spec-clean (not rpm-spec-clean))
  (rpm-update-mode-name)
  (message (concat "Turned `--clean' "
                   (if rpm-spec-clean "on" "off") ".")))

(defun rpm-toggle-test (&optional arg)
  "Toggle rpm-spec-test."
  (interactive "p")
  (setq rpm-spec-test (not rpm-spec-test))
  (rpm-update-mode-name)
  (message (concat "Turned `--test' "
                   (if rpm-spec-test "on" "off") ".")))

(defun rpm-toggle-sign-gpg (&optional arg)
  "Toggle rpm-spec-sign-gpg."
  (interactive "p")
  (setq rpm-spec-sign-gpg (not rpm-spec-sign-gpg))
  (rpm-update-mode-name)
  (message (concat "Turned `--sign' "
                   (if rpm-spec-sign-gpg "on" "off") ".")))

(defun rpm-toggle-add-attr (&optional arg)
  "Toggle rpm-spec-add-attr."
  (interactive "p")
  (setq rpm-spec-add-attr (not rpm-spec-add-attr))
  (rpm-update-mode-name)
  (message (concat "Default add \"attr\" entry turned "
                   (if rpm-spec-add-attr "on" "off") ".")))

(defun rpm-update-mode-name ()
  "Update mode-name according to values set."
  (setq mode-name "RPM-SPEC")
  (setq modes (concat (if rpm-spec-add-attr      "A")
							 (if rpm-spec-clean         "C")
							 (if rpm-spec-sign-gpg      "G")
							 (if rpm-spec-rmsource      "R")
							 (if rpm-spec-short-circuit "S")
							 (if rpm-spec-test          "T")
							 ))
  (if (not (equal modes ""))
		(setq mode-name (concat mode-name ":" modes))))

;;------------------------------------------------------------

(defun rpm-change-timecheck-option (&optional arg)
  "Change the value for timecheck."
  (interactive "p")
  (setq rpm-spec-timecheck
        (read-from-minibuffer "New timecheck: " rpm-spec-timecheck)))

(defun rpm-change-buildroot-option (&optional arg)
  "Change the value for buildroot."
  (interactive "p")
  (setq rpm-spec-buildroot
        (read-from-minibuffer "New buildroot: " rpm-spec-buildroot)))

(defun rpm-change-target-option (&optional arg)
  "Change the value for target."
  (interactive "p")
  (setq rpm-spec-target
        (read-from-minibuffer "New target: " rpm-spec-target)))

(defun rpm-files-umask (&optional arg)
  "Change the default umask for files."
  (interactive "p")
  (setq rpm-default-umask
        (read-from-minibuffer "Default file umask: " rpm-default-umask)))

(defun rpm-files-owner (&optional arg)
  "Change the default owner for files."
  (interactive "p")
  (setq rpm-default-owner
        (read-from-minibuffer "Default file owner: " rpm-default-owner)))

(defun rpm-files-group (&optional arg)
  "Change the source directory."
  (interactive "p")
  (setq rpm-default-group
        (read-from-minibuffer "Default file group: " rpm-default-group)))

(defun rpm-increase-release-tag (&optional arg)
  "Increase the release tag by 1."
  (interactive "p")
  (save-excursion
    (goto-char (point-min))
    (if (search-forward-regexp "^Release:[ \t]*\\([0-9]+\\)\\(.*\\)" nil t)
        (let ((release (1+ (string-to-int (match-string 1)))))
          (setq release (concat (int-to-string release) (match-string 2)))
          (replace-match (concat "Release: " release))
          (message (concat "Release tag changed to " release "."))))
    (if (search-forward-regexp "^Release:[ \t]*%{?\\([^}]*\\)}?$" nil t)
        (rpm-increase-release-with-macros)
      (message "No Release tag found..."))))

;;------------------------------------------------------------

(defun rpm-spec-field-value (field max)
  (save-excursion
    (let ((str
           (progn
             (goto-char (point-min))
             (search-forward-regexp (concat field ":[ \t]*\\(.+\\).*$") max)
             (match-string 1))))
      (if (string-match "%{?\\([^}]*\\)}?$" str)
          (progn
            (goto-char (point-min))
            (search-forward-regexp
             (concat "%define[ \t]+" (substring str (match-beginning 1)
                                                (match-end 1))
                     "[ \t]+\\(.*\\)"))
            (match-string 1))
        str))))

(defun rpm-find-spec-version ()
  (save-excursion
    (goto-char (point-min))
    (let* ((max (search-forward-regexp rpm-section-regexp))
           (version (rpm-spec-field-value "Version" max))
           (release (rpm-spec-field-value "Release" max)) )
      (concat version "-" release))))

(defun rpm-increase-release-with-macros ()
  (save-excursion
    (let ((str
           (progn
             (goto-char (point-min))
             (search-forward-regexp (concat "Release:[ \t]*\\(.+\\).*$") nil)
             (match-string 1))))
      (let ((inrel
             (if (string-match "%{?\\([^}]*\\)}?$" str)
                 (progn
                   (goto-char (point-min))
                   (setq macros (substring str (match-beginning 1)
                                           (match-end 1)))
                   (search-forward-regexp
                    (concat "%define[ \t]+" macros
                            "[ \t]+\\(\\([0-9]\\|\\.\\)+\\)\\(.*\\)"))
                   (concat macros " " (int-to-string (1+ (string-to-int
                                                          (match-string 1))))
                           (match-string 3)))
               str)))
        (setq dinrel inrel)
        (replace-match (concat "%define " dinrel))
        (message (concat "Release tag changed to " dinrel "."))))))

;;------------------------------------------------------------

(defun rpm-spec-initialize ()
  "Create a default spec file if one does not exist or is empty."
  (let (file name version (release "1"))
    (setq file (if (buffer-file-name)
                   (file-name-nondirectory (buffer-file-name))
                 (buffer-name)))
    (cond
     ((eq (string-match "\\(.*\\)-\\([^-]*\\)-\\([^-]*\\).spec" file) 0)
      (setq name (match-string 1 file))
      (setq version (match-string 2 file))
      (setq release (match-string 3 file)))
     ((eq (string-match "\\(.*\\)-\\([^-]*\\).spec" file) 0)
      (setq name (match-string 1 file))
      (setq version (match-string 2 file)))
     ((eq (string-match "\\(.*\\).spec" file) 0)
      (setq name (match-string 1 file))))
    
    (insert
     "Summary: "
     "\nName: " (or name "")
     "\nVersion: " (or version "")
     "\nRelease: " (or release "")
     "\nURL: "
     "\nSource0: %{name}-%{version}.tar.gz"
     "\nLicense: \nGroup: "
     "\nBuildRoot: %{_tmppath}/%{name}-root"
     "\n\n%description\n"
     "\n%prep"
     "\n%setup -q"
     "\n\n%build"
     "\n\n%install"
     "\nrm -rf $RPM_BUILD_ROOT"
     "\n\n%clean"
     "\nrm -rf $RPM_BUILD_ROOT"
     "\n\n%files"
     "\n%defattr(-,root,root)\n" 
     "\n\n%changelog\n")
            
    (rpm-add-change-log-entry "Initial build.\n")))

;;------------------------------------------------------------

(defun rpm-about-rpm-spec-mode (&optional arg)
  "About rpm-spec-mode."
  (interactive "p")
  (message "Made by Stig Bjørlykke, <stigb@tihlde.org>"))

(provide 'rpm-spec-mode)

;;; rpm-spec-mode.el ends here
