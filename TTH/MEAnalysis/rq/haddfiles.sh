#!/bin/bash
hadd -f $1 `cat $2 | xargs`
