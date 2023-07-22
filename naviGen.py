# -*- coding: utf-8 -*-
# Generate a fucking simple navigator (and usually the generated pages are not used as navigator)
# ! Do not reconstruct the template file!!
# v1.0.0: 2018.02.01
# v1.0.1: 2023.07.18 - change to Python3.x; works well in NT; URL optimized

import datetime

NAME_TEMPLATE = 'template.htm'
NAME_SITES = 'sites.txt'
NAME_OUTPUT = 'index.htm'

def timeNow():
	now = datetime.datetime.now()
	return now.strftime("%Y.%m.%d")

def getTemplateFromFile(fname):
	with open(fname, 'rb') as o:
		buf = o.read()
	return buf.decode('utf-8')

def multiReplace(origin, mapList):
	# mapList: {wordOri: wordChange, ...}
	for i in mapList.keys():
		origin = origin.replace(i, mapList[i])
	return origin

def indexGen():
	HTM_CLASSIFY = '<td width="%d%%" height="0" nowrap><div align="center"><a href="#%s">%s</a></div></td>'
	HTM_ITEM = '	<td width="25%%" nowrap><a href="%s" target="_blank">%s</a></td>'
	HTM_VOID = '	<td width="25%" nowrap>&nbsp;</td>\n'
	HTM_GROUP = '''
<tr align="center" valign="middle" bgcolor="#BBBBBB">
	<td colspan="4" nowrap><div align="left">%s<a name="%s"></a></div></td>
</tr>
<tr align="center" valign="middle" bgcolor="#CCCCCC">'''

	template = getTemplateFromFile(NAME_TEMPLATE)

	classes = []

	strGroup = ''
	strIndex = ''

	with open(NAME_SITES, 'rb') as o:
		count = 0
		while True:
			buf = o.readline().decode('utf-8').strip()

			# Special situation
			if buf == '' or buf[0] == '/':
				continue
			if buf == 'EOF':
				if count != 0:
					for i in range(4-count):
						strGroup += HTM_VOID
					count = 0
					strGroup += '</tr>\n'
				break

			# Meet a new classify
			if buf[0] == '#':
				classes.append(buf[1:])
				# Make sure that only 4 items in a row
				if count != 0:
					for i in range(4-count):
						strGroup += HTM_VOID
					count = 0
					strGroup += '</tr>\n'
				strGroup += (HTM_GROUP % (buf[1:], buf[1:]) + '\n')
			else:
				[tag, url] = buf.split(': ')
				strGroup += (HTM_ITEM % (url, tag) + '\n')
				count += 1
				if count == 4:
					# Fill the blank
					strGroup += '</tr>\n<tr align="center" valign="middle" bgcolor="#CCCCCC">\n'
					count = 0

	widthPerIndex = int(1.0 / len(classes) * 100)
	for c in classes:
		strIndex += (HTM_CLASSIFY % (widthPerIndex, c, c) + '\n')

	mapRelation = {
		'$[CLASSIFY]': strIndex,
		'$[GROUP]': strGroup,
		'$[UPDATE]': str(timeNow())
	}
	whole = multiReplace(template, mapRelation)
	return whole

def main():
	with open(NAME_OUTPUT, 'wb') as o:
		o.write(indexGen().encode('utf-8'))

if __name__ == '__main__':
	main()