# Makefile for source rpm: emacs
# $Id$
NAME := emacs
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
