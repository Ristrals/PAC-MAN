#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   error.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/18 10:42:16 by junruan             #+#    #+#            #
#   Updated: 2026/08/18 10:42:55 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Custom exceptions raised by the PacMan."""


class ParsingError(Exception):
    """Raised when the input map file has invalid syntax."""
