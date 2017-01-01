# Copyright (C) 2017 Sergej Alikov <sergej.alikov@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from django.test import TestCase
from django.template import Context, Template


class BlogTemplatetagsTestCase(TestCase):
    def test_md_as_html5(self):

        body = """# H1 heading

**Paragraph** text
<strong>html markup works</strong>
## H2 heading

~~~~{.python}
if True:
  print("Some <b>Python</b> code in markdown")
~~~~

1 First
2. Second
  * sub
3. Last"""

        expected = """<h1>H1 heading</h1>
<p><strong>Paragraph</strong> text
<strong>html markup works</strong></p>
<h2>H2 heading</h2>
<pre><code class="python">if True:
  print(&quot;Some &lt;b&gt;Python&lt;/b&gt; code in markdown&quot;)
</code></pre>

<p>1 First
2. Second
  * sub
3. Last</p>"""

        out = Template(
            "{% load markdown %}"
            "{{ body|md_as_html5 }}"
        ).render(Context({'body': body}))

        self.assertEqual(out, expected)
