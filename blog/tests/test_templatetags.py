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
