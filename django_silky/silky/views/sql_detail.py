import re

from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.views.generic import View

from silky.models import SQLQuery


class SQLDetailView(View):
    def _urlify(self, str):
        r = re.compile("(?P<src>/.*\.py)\", line (?P<num>[0-9]+).*")
        m = r.search(str)
        n = 1
        while m:
            group = m.groupdict()
            src = group['src']
            num = group['num']
            start = m.start('src')
            end = m.end('src')
            rep = '<a name={name} href="?pos={pos}&file_path={src}&line_num={num}#{name}">{src}</a>'.format(pos=n,
                                                                                                            src=src,
                                                                                                            num=num,
                                                                                                            name='c%d' % n)
            str = str[:start] + rep + str[end:]
            m = r.search(str)
            n += 1
        return str

    def get(self, request, request_id, sql_id):
        sql_query = SQLQuery.objects.get(pk=sql_id)
        pos = int(request.GET.get('pos', 0))
        file_path = request.GET.get('file_path', '')
        line_num = int(request.GET.get('line_num', 0))
        tb = sql_query.traceback_ln_only
        tb = [mark_safe(x) for x in self._urlify(tb).split('\n')]
        context = {
            'sql_query': sql_query,
            'traceback': tb,
            'pos': pos,
            'line_num': line_num,
            'file_path': file_path
        }
        if pos and file_path and line_num:
            actual_line, code = self._code(file_path, line_num)
            context['code'] = code
            context['actual_line'] = actual_line
        return render_to_response('silky/sql_detail.html', context)

    def _code(self, file_path, line_num):
        actual_line = ''
        lines = ''
        with open(file_path, 'r') as f:
            r = range(max(0, line_num - 10), line_num + 10)
            for i, line in enumerate(f):
                if i in r:
                    lines += line
                if i + 1 == line_num:
                    actual_line = line
        code = lines.split('\n')
        return actual_line, code


    def _code_context(self, file_path, line_num):
        actual_line, code = self._code(file_path, line_num)
        context = {'code': code, 'file_path': file_path, 'line_num': line_num, 'actual_line': actual_line}
        return context