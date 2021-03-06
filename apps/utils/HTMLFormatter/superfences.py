"""
SuperFences.

pymdownx.superfences
Nested Fenced Code Blocks

This is a modification of the original Fenced Code Extension.
Algorithm has been rewritten to allow for fenced blocks in blockquotes,
lists, etc.  And also , allow for special UML fences like 'flow' for flowcharts
and `sequence` for sequence diagrams.

Modified: 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>
---

Fenced Code Extension for Python Markdown
=========================================

This extension adds Fenced Code Blocks to Python-Markdown.

See <https://pythonhosted.org/Markdown/extensions/fenced_code_blocks.html>
for documentation.

Original code Copyright 2007-2008 [Waylan Limberg](http://achinghead.com/).


All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor
from markdown.blockprocessors import CodeBlockProcessor
from markdown import util as md_util
from pymdownx import highlight as hl
import re
import json
from collections import OrderedDict

SOH = '\u0001'
EOT = '\u0004'

PREFIX_CHARS = ('>', ' ', '\t')

RE_NESTED_FENCE_START = re.compile(
    r'''(?x)
    (?P<fence>~{3,}|`{3,})[ \t]*                                              # Fence opening
    (\{?                                                                      # Language opening
    \.?(?P<lang>[\w#.+-]*))?[ \t]*                                            # Language
    (?:
    hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot)[ \t]*|                   # highlight lines
    toolsbar=(?P<quot1>"|')(?P<toolsbar>.*?)(?P=quot1)[ \t]*|                 # toolsbar
    folded=(?P<quot4>"|')(?P<folded>.*?)(?P=quot4)[ \t]*|                     # code fold
    linefeed=(?P<quot5>"|')(?P<linefeed>.*?)(?P=quot5)[ \t]*|                 # code linefeed
    shownum=(?P<quot6>"|')(?P<shownum>.*?)(?P=quot6)[ \t]*|                   # show code line number
    linenums=(?P<quot2>"|')                                                   # Line numbers
        (?P<linestart>[\d]+)                                                  #   Line number start
        (?:[ \t]+(?P<linestep>[\d]+))?                                        #   Line step
        (?:[ \t]+(?P<linespecial>[\d]+))?                                     #   Line special
    (?P=quot2)[ \t]*|
    (?P<tab>tab=)(?:(?P<quot3>"|')(?P<tab_title>.*?)(?P=quot3))?[ \t]*   # Tab specifier
    )*
    }?[ \t]*$                                                                 # Language closing
    '''
)

RE_TABS = re.compile(r'((?:<p><superfences>.*?</superfences></p>\s*)+)', re.DOTALL)

TAB = r'''<superfences><input name="__tabs_%%(index)s" type="radio" id="__tab_%%(index)s_%%(tab_index)s" %%(state)s/>
<label for="__tab_%%(index)s_%%(tab_index)s">%(title)s</label>
<div class="superfences-content">%(code)s</div></superfences>'''

NESTED_FENCE_END = r'%s[ \t]*$'


def _escape(txt):
    """Basic html escaping."""

    txt = txt.replace('&', '&amp;')
    txt = txt.replace('<', '&lt;')
    txt = txt.replace('>', '&gt;')
    txt = txt.replace('"', '&quot;')
    return txt


class CodeStash(object):
    """
    Stash code for later retrieval.

    Store original fenced code here in case we were
    too greedy and need to restore in an indented code
    block.
    """

    def __init__(self):
        """Initialize."""

        self.stash = {}

    def __len__(self):  # pragma: no cover
        """Length of stash."""

        return len(self.stash)

    def get(self, key, default=None):
        """Get the code from the key."""

        code = self.stash.get(key, default)
        return code

    def remove(self, key):
        """Remove the stashed code."""

        del self.stash[key]

    def store(self, key, code, indent_level):
        """Store the code in the stash."""

        self.stash[key] = (code, indent_level)

    def clear_stash(self):
        """Clear the stash."""

        self.stash = {}


def fence_code_format(source, language, css_class):
    """Format source as code blocks."""

    return '<pre class="%s"><code>%s</code></pre>' % (css_class, _escape(source))


def fence_div_format(source, language, css_class):
    """Format source as div."""

    return '<div class="%s">%s</div>' % (css_class, _escape(source))


class SuperFencesCodeExtension(Extension):
    """SuperFences code block extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.superfences = []
        self.config = {
            'disable_indented_code_blocks': [False, "Disable indented code blocks - Default: False"],
            'custom_fences': [
                [
                    {'name': 'flow', 'class': 'uml-flowchart'},
                    {'name': 'sequence', 'class': 'uml-sequence-diagram'}
                ],
                'Specify custom fences. Default: See documentation.'
            ],
            'highlight_code': [True, "Highlight code - Default: True"],
            'css_class': [
                '',
                "Set class name for wrapper element. The default of CodeHilite or Highlight will be used"
                "if nothing is set. - "
                "Default: ''"
            ],
            'global_toolsbar': [
                '',
                "Config toolsbar menu for global toolsbar, format like this:"
                """
                    {
                        "title": "A Special Title",
                        "copy": {
                            "class": "copy_class",
                            "id": "button-copy",
                            "title": "Click to copy code",
                            "text": "Copy",
                            "icon": "i-icon-copy",
                            "event": "onclick='copyCode(this)'"},
                        "break": {
                            "class": "break_class",
                            "id": "button-break",
                            "title": "Click to break or no break line",
                            "text": "Break",
                            "icon": "i-icon-break",
                            "event": "onclick='breakCode(this)'"},
                        "fold": {
                            "class": "fold_class",
                            "id": "button-fold",
                            "title": "Click to fold code",
                            "text": "Fold",
                            "icon": "i-icon-fold",
                            "event": "onclick='foldCode(this)'"
                        }
                    }
                """
                "`title` is indigenous to assign title to toolsbar, if no pass it will use language name."
            ],
            'toolsbarclass': ['toolsbar'],
            'preserve_tabs': [False, "Preserve tabs in fences - Default: False"]
        }
        super(SuperFencesCodeExtension, self).__init__(*args, **kwargs)

    def extend_super_fences(self, name, formatter):
        """Extend SuperFences with the given name, language, and formatter."""

        self.superfences.append(
            {
                "name": name,
                "test": lambda l, language=name: language == l,
                "formatter": formatter
            }
        )

    def extendMarkdown(self, md, md_globals):
        """Add fenced block preprocessor to the Markdown instance."""

        # Not super yet, so let's make it super
        md.registerExtension(self)
        config = self.getConfigs()

        # Default fenced blocks
        self.superfences.insert(
            0,
            {
                "name": "superfences",
                "test": lambda language: True,
                "formatter": None
            }
        )

        # UML blocks
        custom_fences = config.get('custom_fences', [])
        for custom in custom_fences:
            name = custom.get('name')
            class_name = custom.get('class')
            fence_format = custom.get('format', fence_code_format)
            if name is not None and class_name is not None:
                self.extend_super_fences(
                    name,
                    lambda s, l, c=class_name, f=fence_format: f(s, l, c)
                )

        self.markdown = md
        self.patch_fenced_rule()
        for entry in self.superfences:
            entry["stash"] = CodeStash()

    def patch_fenced_rule(self):
        """
        Patch Python Markdown with our own fenced block extension.

        We don't attempt to protect against a user loading the `fenced_code` extension with this.
        Most likely they will have issues, but they shouldn't have loaded them together in the first place :).
        """

        config = self.getConfigs()
        fenced = SuperFencesBlockPreprocessor(self.markdown)
        indented_code = SuperFencesCodeBlockProcessor(self)
        fenced.config = config
        fenced.extension = self
        indented_code.config = config
        indented_code.markdown = self.markdown
        indented_code.extension = self
        self.superfences[0]["formatter"] = fenced.highlight
        self.markdown.parser.blockprocessors['code'] = indented_code
        if config["preserve_tabs"]:
            self.markdown.preprocessors.add('fenced_code_block', fenced, "<normalize_whitespace")
            post_fenced = SuperFencesBlockPostNormalizePreprocessor(self.markdown)
            self.markdown.preprocessors.add('fenced_code_post_norm', post_fenced, ">normalize_whitespace")
        else:
            self.markdown.preprocessors.add('fenced_code_block', fenced, ">normalize_whitespace")
        self.markdown.postprocessors.add('fenced_tabs', SuperFencesTabPostProcessor(self.markdown), '>raw_html')

    def reset(self):
        """Clear the stash."""

        for entry in self.superfences:
            entry["stash"].clear_stash()


class SuperFencesTabPostProcessor(Postprocessor):
    """Post processor for grouping tabs."""

    def repl(self, m):
        """Replace grouped superfences tabs with a tab group."""

        self.count += 1
        tab_count = 0
        tabs = []
        for entry in [x.strip() for x in m.group(1).split('</superfences></p>')]:
            tabs.append(
                entry.replace('<p><superfences>', '') % {
                    'index': self.count,
                    'tab_index': tab_count,
                    'state': ('checked="checked" ' if tab_count == 0 else ''),
                    'tab_title': 'Tab %d' % (tab_count + 1)
                }
            )
            tab_count += 1
        return '<div class="superfences-tabs">\n' + '\n'.join(tabs) + '</div>\n'

    def run(self, text):
        """Search for superfences tab and group consecutive tabs together."""

        self.count = 0
        return RE_TABS.sub(self.repl, text)


class SuperFencesBlockPostNormalizePreprocessor(Preprocessor):
    """Preprocessor to clean up normalization bypass hack."""

    TEMP_PLACEHOLDER_RE = re.compile(
        r'^([\> ]*)%s(%s)%s$' % (
            SOH,
            md_util.HTML_PLACEHOLDER[1:-1] % r'([0-9]+)',
            EOT
        )
    )

    def run(self, lines):
        """Search for fenced blocks."""

        new_lines = []
        for line in lines:
            line = self.TEMP_PLACEHOLDER_RE.sub(r'\1' + md_util.STX + r'\2' + md_util.ETX, line)
            new_lines.append(line)

        return new_lines


class SuperFencesBlockPreprocessor(Preprocessor):
    """
    Preprocessor to find fenced code blocks.

    Because this is done as a preprocessor, it might be too greedy.
    We will stash the blocks code and restore if we mistakenly processed
    text from an indented code block.
    """

    CODE_WRAP = '<pre%s><code%s>%s</code></pre>'

    def __init__(self, md):
        """Initialize."""

        super(SuperFencesBlockPreprocessor, self).__init__(md)
        self.markdown = md
        self.tab_len = self.markdown.tab_length
        self.checked_hl_settings = False
        self.checked_global_toolsbar = False
        self.codehilite_conf = {}

    def normalize_ws(self, text):
        """Normalize whitespace."""

        return text.expandtabs(self.tab_len)

    def rebuild_block(self, lines):
        """Dedent the fenced block lines."""

        return '\n'.join([line[self.ws_virtual_len:] for line in lines])

    def get_hl_settings(self):
        """Check for CodeHilite extension to get its config."""

        if not self.checked_hl_settings:
            self.checked_hl_settings = True
            self.highlight_code = self.config['highlight_code']

            config = hl.get_hl_settings(self.markdown)
            css_class = self.config['css_class']
            self.css_class = css_class if css_class else config['css_class']

            self.extend_pygments_lang = config.get('extend_pygments_lang', None)
            self.guess_lang = config['guess_lang']
            self.pygments_style = config['pygments_style']
            self.use_pygments = config['use_pygments']
            self.noclasses = config['noclasses']
            self.linenums = config['linenums']

    def build_global_toolsbar(self, language):
        """
        build global toolsbar
        :return:
        """
        if not self.checked_global_toolsbar:
            self.checked_global_toolsbar = True
            # toolsbar wrap class
            toolsbarclass = self.config['toolsbarclass']
            self.toolsbarclass = self._decodeifneeded(toolsbarclass) if toolsbarclass else 'toolsbar'
            # build global toolsbar
            self.global_toolsbar = self._get_opt_checked_if_multitype(self.config['global_toolsbar'], False)
            self.global_toolsbar = self._build_toolsbar(self.global_toolsbar, language)

    def clear(self):
        """Reset the class variables."""

        self.ws = None
        self.ws_len = 0
        self.ws_virtual_len = 0
        self.fence = None
        self.lang = None
        self.hl_lines = None
        self.linestart = None
        self.linestep = None
        self.linespecial = None
        self.folded = None
        self.linefeed = None
        self.shownum = None
        self.quote_level = 0
        self.code = []
        self.empty_lines = 0
        self.fence_end = None
        self.tab = None

    def eval_fence(self, ws, content, start, end):
        """Evaluate a normal fence."""

        if (ws + content).strip() == '':
            # Empty line is okay
            self.empty_lines += 1
            self.code.append(ws + content)
        elif len(ws) != self.ws_virtual_len and content != '':
            # Not indented enough
            self.clear()
        elif self.fence_end.match(content) is not None and not content.startswith((' ', '\t')):
            # End of fence
            self.process_nested_block(ws, content, start, end)
        else:
            # Content line
            self.empty_lines = 0
            self.code.append(ws + content)

    def eval_quoted(self, ws, content, quote_level, start, end):
        """Evaluate fence inside a blockquote."""

        if quote_level > self.quote_level:
            # Quote level exceeds the starting quote level
            self.clear()
        elif quote_level <= self.quote_level:
            if content == '':
                # Empty line is okay
                self.code.append(ws + content)
                self.empty_lines += 1
            elif len(ws) < self.ws_len:
                # Not indented enough
                self.clear()
            elif self.empty_lines and quote_level < self.quote_level:
                # Quote levels don't match and we are signified
                # the end of the block with an empty line
                self.clear()
            elif self.fence_end.match(content) is not None:
                # End of fence
                self.process_nested_block(ws, content, start, end)
            else:
                # Content line
                self.empty_lines = 0
                self.code.append(ws + content)

    def get_tab(self, code, title):
        """Wrap code in tab div."""

        return TAB % {'code': code.replace('%', '%%'), 'title': title}

    def process_nested_block(self, ws, content, start, end):
        """Process the contents of the nested block."""

        self.last = ws + self.normalize_ws(content)
        code = None
        for entry in reversed(self.extension.superfences):
            if entry["test"](self.lang):
                code = entry["formatter"](self.rebuild_block(self.code), self.lang)
                if self.tab is not None:
                    code = self.get_tab(code, self.tab)
                break

        if code is not None:
            self._store(self.normalize_ws('\n'.join(self.code)) + '\n', code, start, end, entry)
        self.clear()

    def parse_folded(self, folded):
        return bool(int(folded)) if folded else False

    def parse_linefeed(self, linefeed):
        return bool(int(linefeed)) if linefeed else True

    def parse_shownum(self, shownum):
        return bool(int(shownum)) if shownum else True

    def parse_hl_lines(self, hl_lines):
        """Parse the lines to highlight."""

        return list(map(int, hl_lines.strip().split())) if hl_lines else []

    def parse_line_start(self, linestart):
        """Parse line start."""

        return int(linestart) if linestart else -1

    def parse_line_step(self, linestep):
        """Parse line start."""

        step = int(linestep) if linestep else -1

        return step if step > 1 else -1

    def parse_line_special(self, linespecial):
        """Parse line start."""

        return int(linespecial) if linespecial else -1

    def parse_fence_line(self, line):
        """Parse fence line."""

        ws_len = 0
        ws_virtual_len = 0
        ws = []
        index = 0
        for c in line:
            if ws_virtual_len >= self.ws_virtual_len:
                break
            if c not in PREFIX_CHARS:
                break
            ws_len += 1
            if c == '\t':
                tab_size = self.tab_len - (index % self.tab_len)
                ws_virtual_len += tab_size
                ws.append(' ' * tab_size)
            else:
                tab_size = 1
                ws_virtual_len += 1
                ws.append(c)
            index += tab_size

        return ''.join(ws), line[ws_len:]

    def parse_whitespace(self, line):
        """Parse the whitespace (blockquote syntax is counted as well)."""

        self.ws_len = 0
        self.ws_virtual_len = 0
        ws = []
        for c in line:
            if c not in PREFIX_CHARS:
                break
            self.ws_len += 1
            ws.append(c)

        ws = self.normalize_ws(''.join(ws))
        self.ws_virtual_len = len(ws)

        return ws

    def search_nested(self, lines):
        """Search for nested fenced blocks."""

        count = 0
        for line in lines:
            if self.fence is None:
                ws = self.parse_whitespace(line)

                # Found the start of a fenced block.
                m = RE_NESTED_FENCE_START.match(line, self.ws_len)
                if m is not None:
                    start = count
                    self.first = ws + self.normalize_ws(m.group(0))
                    self.ws = ws
                    self.quote_level = self.ws.count(">")
                    self.empty_lines = 0
                    self.fence = m.group('fence')
                    self.lang = m.group('lang')
                    self.hl_lines = m.group('hl_lines')
                    self.linestart = m.group('linestart')
                    self.linestep = m.group('linestep')
                    self.linespecial = m.group('linespecial')
                    self.toolsbar = m.group('toolsbar')
                    self.folded = m.group('folded')
                    self.linefeed = m.group('linefeed')
                    self.shownum = m.group('shownum')
                    self.fence_end = re.compile(NESTED_FENCE_END % self.fence)
                    if m.group('tab'):
                        self.tab = m.group('tab_title')
                        if not self.tab:
                            self.tab = self.lang
                        if not self.tab:
                            self.tab = '%(tab_title)s'
            else:
                # Evaluate lines
                # - Determine if it is the ending line or content line
                # - If is a content line, make sure it is all indentend
                #   with the opening and closing lines (lines with just
                #   whitespace will be stripped so those don't matter).
                # - When content lines are inside blockquotes, make sure
                #   the nested block quote levels make sense according to
                #   blockquote rules.
                ws, content = self.parse_fence_line(line)

                end = count + 1
                quote_level = ws.count(">")

                if self.quote_level:
                    # Handle blockquotes
                    self.eval_quoted(ws, content, quote_level, start, end)
                elif quote_level == 0:
                    # Handle all other cases
                    self.eval_fence(ws, content, start, end)
                else:
                    # Looks like we got a blockquote line
                    # when not in a blockquote.
                    self.clear()

            count += 1

        # Now that we are done iterating the lines,
        # let's replace the original content with the
        # fenced blocks.
        while len(self.stack):
            fenced, start, end = self.stack.pop()
            if self.preserve_tabs:
                lines = lines[:start] + [fenced.replace(md_util.STX, SOH, 1)[:-1] + EOT] + lines[end:]
            else:
                lines = lines[:start] + [fenced] + lines[end:]
        return lines

    def highlight(self, src, language):
        """
        Syntax highlight the code block.

        If config is not empty, then the CodeHilite extension
        is enabled, so we call into it to highlight the code.
        """

        if self.highlight_code:
            linestep = self.parse_line_step(self.linestep)
            linestart = self.parse_line_start(self.linestart)
            linespecial = self.parse_line_special(self.linespecial)
            hl_lines = self.hl_lines  # self.parse_hl_lines(self.hl_lines)
            linefeed = self.parse_linefeed(self.linefeed)
            shownum = self.parse_shownum(self.shownum)

            el = hl.Highlight(
                guess_lang=self.guess_lang,
                pygments_style=self.pygments_style,
                use_pygments=self.use_pygments,
                noclasses=self.noclasses,
                linenums=self.linenums,
                extend_pygments_lang=self.extend_pygments_lang
            ).highlight(
                src,
                language,
                self.css_class,
                hl_lines=hl_lines,
                linestart=linestart,
                linestep=linestep,
                linespecial=linespecial,
                linefeed=linefeed,
                shownum=shownum
            )
            # fence toolsbar
            el = self.fence_toolbar_format(el, language)
        else:
            # Format as a code block.
            el = self.CODE_WRAP % ('', '', _escape(src))
        return el

    def _decodeifneeded(self, value):
        if isinstance(value, bytes):
            if self.encoding:
                return value.decode(self.encoding)
            return value.decode()
        return value

    def _get_opt_checked_if_multitype(self, opt, default):
        """
        check option type, for string, list, tuple and dict.
        :param opt: option
        :param default: default value
        :return: if the length of string, dict, list, tuple or dict's keys is not zero return result, else default value.
        """
        if not opt:
            return default
        try:
            option = json.loads(opt, object_pairs_hook=OrderedDict)
            return option if len(option.keys()) > 0 else default
        except Exception:
            pass
        try:
            option = json.dump(opt)
            return option if len(option.keys()) > 0 else default
        except Exception:
            pass
        if isinstance(opt, (str,)):
            return opt if len(opt) > 0 else default
        if isinstance(opt, (dict,)):
            return opt if len(opt.keys()) > 0 else default
        elif isinstance(opt, (list, tuple)):
            option = list(opt)
            return option if len(option) > 0 else default
        else:
            raise ValueError("Invalid value; please check the option's type, allow for str, list, tuple and dict")

    def _build_toolsbar(self, toolsbar, language):
        """
        build toolsbar div according to a toolsbar dict
        :param toolsbar: a dict special toolsbar, like this:
                {
                    "title": "A Special Title",
                    "copy": {
                        "class": "copy_class",
                        "id": "button-copy",
                        "title": "Copy",
                        "icon": "i-icon-copy",
                        "event": "onclick='copyCode(this)'"
                    },
                    "wrap": {
                        "class": "wrap_class",
                        "id": "button-wrap",
                        "title": "Wrap",
                        "icon": "i-icon-wrap",
                        "event": "onclick='wrapCode(this)'"
                    },
                    "fold": {
                        "class": "fold_class",
                        "id": "button-fold",
                        "title": "fold",
                        "icon": "i-icon-fold",
                        "event": "onclick='foldCode(this)'"
                    }
                }
        :return: a toolsbar div block if success or a empty str if failed
        """
        if isinstance(toolsbar, (dict,)) and len(toolsbar.keys()) > 0:
            # ??????div
            toolsbardiv = '<div'
            divstyles = []
            if self.noclasses:
                divstyles.append('display: flex')
                divstyles.append('justify-content: flex-end')
                divstyles.append('height: 20px')
                divstyles.append('border: 1px solid #ccc')
                divstyles.append('background: #eee')
                divstyles.append('padding:2px')
                toolsbardiv = toolsbardiv + (divstyles and ' style="%s"' % ';'.join(divstyles)) + '>'
            else:
                toolsbardiv = toolsbardiv + (self.toolsbarclass and ' class="%s"' % self.toolsbarclass) + '>'

            # ????????????
            titleSpan = '<span'
            spanstyles = []
            if self.noclasses:
                spanstyles.append('flex-grow: 1')
                spanstyles.append('color: #666')
                spanstyles.append('font-size: 13px')
                spanstyles.append('padding-left: 4px')
                titleSpan = titleSpan + (spanstyles and ' style="%s"' % ';'.join(spanstyles)) + '>'
            else:
                titleSpan = titleSpan + ' class="language">'

            # ??????
            title = ''
            if 'title' in toolsbar.keys():
                title = toolsbar['title']
            elif isinstance(language, (str,)) and len(str(language)) > 0:
                title = language.capitalize()
            titleSpan = titleSpan + title + '</span>'

            buttons = []
            # ????????????
            # <button class="copy" id="copy" value="??????" type="button" title="??????" onclick="copyCode(this)">??????</button>
            for name, tool in toolsbar.items():
                if name == 'title':
                    continue
                clazz = tool['class'] if 'class' in tool else ''
                iD = tool['id'] if 'id' in tool else ''
                title = tool['title'] if 'title' in tool else ''
                text = tool['text'] if 'text' in tool else ''
                icon = tool['icon'] if 'icon' in tool else ''
                event = tool['event'] if 'event' in tool else ''

                button = '<button'
                # clazz
                buttonstyles = []
                if self.noclasses:
                    buttonstyles.append('border: 1px solid #ccc')
                    buttonstyles.append('margin-left: 1px')
                    buttonstyles.append('outline: none')
                    button = button + (buttonstyles and ' style="%s"' % ';'.join(buttonstyles))
                else:
                    button = button + (clazz and ' class="%s"' % clazz)
                # id
                button = button + (iD and ' id="%s"' % iD)
                # value
                button = button + (title and ' value="%s"' % title)
                # title
                button = button + (title and ' title="%s"' % title)
                # onclick
                button = button + (title and ' %s' % event)
                # type
                button = button + 'type="button">'
                # text
                button = button + text + '</button>'
                buttons.append(button)
            buttons = ''.join(buttons)
            return toolsbardiv + titleSpan + buttons + '</div>'
        else:
            return ''

    def fence_toolbar_format(self, formatted_code, language):
        """
        ????????????toolbar
        :param formatted_code: ??????highlight??????????????????
        :param language: ??????
        :return:
        """
        if len(formatted_code) == 0:
            return formatted_code

        # ????????????????????????
        local_toolsbar = self._get_opt_checked_if_multitype(self.toolsbar, False)

        # if False, no toolsbar for this sinppet
        if not local_toolsbar:
            return formatted_code

        # code fold and linefeed
        wrapclasses = []
        if not self.noclasses and self.parse_linefeed(self.linefeed):
            wrapclasses.append('linefeed')
        if not self.noclasses and self.parse_folded(self.folded):
            wrapclasses.append('folded')
        if not self.noclasses and self.parse_shownum(self.shownum):
            wrapclasses.append('shownum')

        # if global, use global toolsbar
        if 'global' in local_toolsbar:
            title = ''
            if 'title' in local_toolsbar and isinstance(local_toolsbar, (dict,)):
                title = local_toolsbar['title']
            elif isinstance(language, (str,)) and len(str(language)) > 0:
                # refresh language identifier
                title = language.capitalize()
            pattern = re.compile(r'(<span[^>]*>).*?(</span>)', re.S | re.M)
            self.global_toolsbar = pattern.sub(r'\1' + title + r'\2', self.global_toolsbar)
            if not self.noclasses:
                wrapclasses.append('with-global-toolsbar')
            return '<div%s>%s%s</div>' % (wrapclasses and ' class="%s"' % ' '.join(wrapclasses),
                                          self.global_toolsbar, formatted_code)

        # or use local globar only for this sinppet
        local_toolsbar = self._build_toolsbar(local_toolsbar, language)
        if not self.noclasses:
            wrapclasses.append('with-local-toolsbar')
        return '<div%s>%s%s</div>' % (wrapclasses and ' class="%s"' % ' '.join(wrapclasses),
                                      local_toolsbar, formatted_code)

    def _store(self, source, code, start, end, obj):
        """
        Store the fenced blocks in the stack to be replaced when done iterating.

        Store the original text in case we need to restore if we are too greedy.
        """
        # Save the fenced blocks to add once we are done iterating the lines
        placeholder = self.markdown.htmlStash.store(code, safe=True)
        self.stack.append(('%s%s' % (self.ws, placeholder), start, end))
        if not self.disabled_indented:
            # If an indented block consumes this placeholder,
            # we can restore the original source
            obj["stash"].store(
                placeholder[1:-1],
                "%s\n%s%s" % (self.first, self.normalize_ws(source), self.last),
                self.ws_virtual_len
            )

    def run(self, lines):
        """Search for fenced blocks."""

        self.get_hl_settings()
        self.build_global_toolsbar(None)
        self.clear()
        self.stack = []
        self.disabled_indented = self.config.get("disable_indented_code_blocks", False)
        self.preserve_tabs = self.config.get("preserve_tabs", False)

        lines = self.search_nested(lines)

        return lines


class SuperFencesCodeBlockProcessor(CodeBlockProcessor):
    """Process indented code blocks to see if we accidentally processed its content as a fenced block."""

    FENCED_BLOCK_RE = re.compile(
        r'^([\> ]*)%s(%s)%s$' % (
            md_util.HTML_PLACEHOLDER[0],
            md_util.HTML_PLACEHOLDER[1:-1] % r'([0-9]+)',
            md_util.HTML_PLACEHOLDER[-1]
        )
    )

    def test(self, parent, block):
        """Test method that is one day to be deprecated."""

        return True

    def reindent(self, text, pos, level):
        """Reindent the code to where it is supposed to be."""

        indented = []
        for line in text.split('\n'):
            index = pos - level
            indented.append(line[index:])
        return '\n'.join(indented)

    def revert_greedy_fences(self, block):
        """Revert a prematurely converted fenced block."""

        new_block = []
        for line in block.split('\n'):
            m = self.FENCED_BLOCK_RE.match(line)
            if m:
                key = m.group(2)
                indent_level = len(m.group(1))
                original = None
                for entry in self.extension.superfences:
                    stash = entry["stash"]
                    original, pos = stash.get(key)
                    if original is not None:
                        code = self.reindent(original, pos, indent_level)
                        new_block.append(code)
                        stash.remove(key)
                        break
                if original is None:  # pragma: no cover
                    # Too much work to test this. This is just a fall back in case
                    # we find a placeholder, and we went to revert it and it wasn't in our stash.
                    # Most likely this would be caused by someone else. We just want to put it
                    # back in the block if we can't revert it.  Maybe we can do a more directed
                    # unit test in the future.
                    new_block.append(line)
            else:
                new_block.append(line)
        return '\n'.join(new_block)

    def run(self, parent, blocks):
        """Look for and parse code block."""

        handled = False

        if not self.config.get("disable_indented_code_blocks", False):
            handled = CodeBlockProcessor.test(self, parent, blocks[0])
            if handled:
                if self.config.get("nested", True):
                    blocks[0] = self.revert_greedy_fences(blocks[0])
                handled = CodeBlockProcessor.run(self, parent, blocks) is not False
        return handled


def makeExtension(*args, **kwargs):
    """Return extension."""

    return SuperFencesCodeExtension(*args, **kwargs)
