# -*- coding: utf-8 -*-
import win32com.client  # pywin32의 모듈
import pythoncom
import scolor, jfinder

class han:
	def __init__(self, file_name=""):

		self.color = scolor.scolor()
		self.jf = jfinder.jfinder()

		if file_name=="":
			self.active_doc()
		elif file_name=="new":
			self.han_program = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
			self.han_program.XHwpWindows.Item(0).Visible = 1
		else:
			self.han_program = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
			self.han_program.RegisterModule("FilePathCheckDLL", "AutomationModule")
			self.han_program.XHwpWindows.Item(0).Visible = 1
			self.han_program.Open(file_name)


	def manual(self):
		result = """
		커서 : 캐롯의 의미
		커서의 위치 : 선택영역에서, 제일 앞부분의 글자위치
		단어 : (단어+ 뒤의공백)까지를 포함한것
		글 : 커서 뒤의 글자
		"""
		return result


	def active_doc(self):
		"""
		현재 오픈된 한글 문서의 객체를 갖고온다
		"""
		context = pythoncom.CreateBindCtx(0)
		running_coms = pythoncom.GetRunningObjectTable()
		monikers = running_coms.EnumRunning()
		for moniker in monikers:
			name = moniker.GetDisplayName(context, moniker)
			if "hwp" in str(name).lower():
				obje = running_coms.GetObject(moniker)
				self.han_program = win32com.client.Dispatch(obje.QueryInterface(pythoncom.IID_IDispatch))
				self.han_program.XHwpWindows.Item(0).Visible = 1
		return self.han_program

	def close(self):
		self.han_program.Clear(3)
		self.han_program.Quit()

	def copy(self):
		"""
		복사하기
		"""
		self.han_program.HAction.Run('Copy')

	def count_char_in_doc(self):
		"""
		문서 전체의 글자갯수 (공백도1개임)
		"""
		act = self.han_program.CreateAction("DocumentInfo")
		set = act.CreateSet()
		act.GetDefault(set)
		set.SetItem("DetailInfo", 1)
		act.Execute(set)

		result = set.Item("DetailCharCount")
		print("문서안의 글자수는 => ", result)
		return result

	def count_char_in_selection(self):
		"""
		선택영역 전체의 글자갯수 (공백도1개임)
		"""
		aaa = self.read_value_in_selection()
		result = len(str(aaa))
		print("선택영역안의 글자수는 => ", result)
		return result

	def count_line_in_doc(self):
		"""
		문서 전체의 줄수
		"""
		act = self.han_program.CreateAction("DocumentInfo")
		set = act.CreateSet()
		act.GetDefault(set)
		set.SetItem("DetailInfo", 1)
		act.Execute(set)

		result = set.Item("DetailLineCount")
		print("문서안의 총 줄수 => ", result)
		return result

	def count_page_in_doc(self):
		"""
		문서안의 총 페이지수
		"""
		act = self.han_program.CreateAction("DocumentInfo")
		set = act.CreateSet()
		act.GetDefault(set)
		set.SetItem("DetailInfo", 1)
		act.Execute(set)

		result = set.Item("DetailPageCount")
		return result

	def count_shape_in_doc(self):
		"""
		문서안의 총 그리기 개체수
		"""
		ctrl = self.han_program.HeadCtrl  # 첫번째 컨트롤(HaedCtrl)부터 탐색 시작.
		count = 0
		while ctrl != None:
			nextctrl = ctrl.Next
			if ctrl.CtrlID == "gso":
				count += 1
			ctrl = nextctrl
		return count

	def count_table_in_doc(self):
		"""
		문서안의 총 테이블수
		"""
		ctrl = self.han_program.HeadCtrl  # 첫번째 컨트롤(HaedCtrl)부터 탐색 시작.
		count = 0
		while ctrl != None:
			nextctrl = ctrl.Next
			if ctrl.CtrlID == "tbl":
				count += 1
			ctrl = nextctrl
		return count

	def count_word_in_doc(self):
		"""
		문서안의 총 단어수
		"""
		act = self.han_program.CreateAction("DocumentInfo")
		set = act.CreateSet()
		act.GetDefault(set)
		set.SetItem("DetailInfo", 1)
		act.Execute(set)

		result = set.Item("DetailWordCount")
		return result

	def count_word_in_selection(self):
		"""
		선택영역안의 단어수
		"""
		aaa = self.read_value_in_selection()
		result = len(str(aaa).split(" "))
		return result

	def data_control_id(self):
		aaa = {
		"cold":["ColDef","단"],
		"secd":["SecDef","구역"],
		"fn":["FootnoteShape","각주"],
		"en":["FootnoteShape","미주"],
		"tbl":["able","표"],
		"eqed":["EqEdit","수식"],
		"gso":["ShapeObject","그리기 개체"],
		"atno":["AutoNum","번호 넣기"],
		"nwno":["AutoNum","새 번호로"],
		"pgct":["PageNumCtrl","페이지 번호 제어 "],
		"pghd":["PageHiding","감추기"],
		"pgnp":["PageNumPos","쪽 번호 위치"],
		"head":["HeaderFooter","머리말"],
		"foot":["HeaderFooter","꼬리말"],
		"%dte":["FieldCtrl","현재의 날짜/시간 필드"],
		"%ddt":["FieldCtrl","파일 작성 날짜/시간 필드"],
		"%pat":["FieldCtrl","문서 경로 필드"],
		"%bmk":["FieldCtrl","블록 책갈피"],
		"%mmg":["FieldCtrl","메일 머지"],
		"%xrf":["FieldCtrl","상호 참조"],
		"%fmu":["FieldCtrl","계산식"],
		"%clk":["FieldCtrl","누름틀"],
		"%smr":["FieldCtrl","문서 요약 정보 필드"],
		"%usr":["FieldCtrl","사용자 정보 필드"],
		"%hlk":["FieldCtrl","하이퍼링크"],
		"bokm":["TextCtrl","책갈피"],
		"idxm":["IndexMark","찾아보기"],
		"tdut":["Dutmal","덧말"],
		"tcmt":["없음","주석"],}

	def delete_current_line_at_cursor(self):
		"""
		현재 커서가있는 라인의 삭제
		"""
		self.han_program.HAction.Run("DeleteLine")

	def delete_char_from_cursor_to_end_of_line(self):
		"""
		현재 커서에서 줄끝가지의 글자를 삭제
		"""
		self.han_program.HAction.Run("DeleteLineEnd")

	def delete_char_from_cursor_to_nth_char(self, input_no):
		"""
		현재 커서에서 n번째 글자까지 삭제
		"""
		self.select_nth_char_from_selection(input_no-1)
		self.han_program.HAction.Run("Delete")

	def delete_header_footer(self):
		"""
		머릿글과 꼬릿글을 삭제
		"""
		return self.han_program.HAction.Run("HeaderFooterDelete")

	def delete_line_by_no(self, input_no):
		"""
		줄번호로 삭제
		"""
		self.move_cursor_to_nth_line_from_begin_of_doc(input_no-1)
		self.han_program.HAction.Run("DeleteLine")

	def delete_para_by_no(self, input_no):
		"""
		문단번호로 삭제
		"""
		self.move_cursor_to_para_by_no(input_no-1)
		self.select_current_para()
		self.han_program.HAction.Run("Delete")

	def delete_word_by_no(self, input_no):
		"""
		단어 번호로 삭제
		"""
		self.select_nth_word_from_begin_of_doc(input_no-1)
		self.han_program.HAction.Run("Delete")

	def delete_previous_word_from_cursor(self):
		"""
		현재커서의 전 단어 삭제
		"""
		self.han_program.HAction.Run("DeleteWordBack")

	def delete_selection(self):
		"""
		선택영역 삭제
		"""
		self.han_program.HAction.Run("Delete")

	def delete_shape_by_no(self, input_no):
		"""
		그리기 객체 번호로 삭제
		"""
		ctrl = self.han_program.HeadCtrl  # 첫번째 컨트롤(HaedCtrl)부터 탐색 시작.
		count = 0

		while ctrl != None:
			nextctrl = ctrl.Next
			if ctrl.CtrlID == "gso":
				print(ctrl.CtrlID,count )
				count += 1
				if input_no == count:
					#self.han_program.SetPosBySet(ctrl.GetAnchorPos(0))
					#self.han_program.FindCtrl()
					self.han_program.DeleteCtrl(ctrl)
					break
			ctrl = nextctrl

	def delete_table_by_no(self, input_no):
		"""
		테이블 번호로 삭제
		"""
		ctrl = self.han_program.HeadCtrl  # 첫번째 컨트롤(HaedCtrl)부터 탐색 시작.
		count = 0

		while ctrl != None:
			nextctrl = ctrl.Next
			if ctrl.CtrlID == "tbl":
				print(ctrl.CtrlID,count )
				count += 1
				if input_no == count:
					#self.han_program.SetPosBySet(ctrl.GetAnchorPos(0))
					#self.han_program.FindCtrl()
					self.han_program.DeleteCtrl(ctrl)
					break
			ctrl = nextctrl

	def delete_one_word_at_cursor(self):
		"""
		커서에서 단어1개 삭제
		"""
		self.han_program.HAction.Run("DeleteWord")

	def delete_xline_in_table(self, table_no, x):
		"""
		테이블의 가로줄 하나 삭제
		"""
		self.select_table_object_by_no(table_no)
		for no in range(x-1):
			self.han_program.Run("TableLowerCell")
		self.han_program.CreateAction("DeleteLine")

	def delete_yline_in_table(self, table_no, y):
		"""
		테이블의 세로줄 하나 삭제
		"""
		self.select_table_object_by_no(table_no)
		self.han_program.Run("ShapeObjTableSelCell")
		for no in range(y-1):
			self.han_program.Run("TableRightCell")
		self.han_program.CreateAction("SelectColumn")
		self.han_program.CreateAction("Delete")

	def draw_outline_in_selection(self):
		"""
		테두리 그리기
		"""
		self.han_program.CreateAction("CharShapeOutline")

	def draw_outside_border_in_selection(self):
		"""
		테두리 그리기
		"""
		self.han_program.CreateAction("CharShapeOutline")

	def draw_strikethrough_in_selection(self):
		"""
		취소선
		"""
		self.han_program.CreateAction("CharShapeCenterline")

	def draw_underline_in_selection(self):
		"""
		밑줄
		"""
		self.han_program.CreateAction("CharShapeUnderline")

	def get_all_document_information(self):
		"""
		기본 문서의 정보
		"""
		action = self.han_program.CreateAction("DocumentInfo")
		para_set = action.CreateSet()
		action.GetDefault(para_set)
		para_set.SetItem("SectionInfo",1)
		result = action.Execute(para_set)
		return result

	def get_char_no_at_cursor(self):
		"""
		커서위치의 글자번호
		"""
		result = self.han_program.KeyIndicator()[6]  # 칸
		#result = self.han_program.GetPos()[2]
		return result

	def get_end_char_no_of_selection(self):
		"""
		선택영역의 끝글자의 번호
		"""
		no1 = self.get_char_no_at_cursor()
		no2 = self.count_char_in_selection()
		return no1 + no2 -1

	def get_start_char_no_of_selection(self):
		"""
		선택영역의 시작 글자의 번호
		"""
		result = self.get_char_no_at_cursor()
		return result

	def get_current_xy_in_table(self):
		"""
		테이블안에 있는 커서의 번호
		"""
		#aaa = self.han_program.KeyIndicator()
		#cell_a1 = aaa.Split('(', ')')[1]

		if not self.han_program.CellShape:  # 표 안에 있을 때만 CellShape 오브젝트를 리턴함
			raise AttributeError("현재 캐럿이 표 안에 있지 않습니다.")
		return self.han_program.KeyIndicator()[-1][1:].split(")")[0]

	def get_line_no_at_cursor(self):
		"""
		커서의 줄번호
		"""
		result = self.han_program.KeyIndicator()[5]  # 줄
		return result

	def get_start_line_no_of_selection(self):
		"""
		선택영역의 첫번째 줄의 번호
		"""
		result = self.get_line_no_at_cursor()
		return result


	def get_page_no_at_cursor(self):
		"""
		현재커서의 페이지 번호
		"""
		result = self.han_program.Item(0).XHwpDocumentInfo.CurrentPage
		return result

	def get_start_page_no_of_selection(self):
		"""
		선택영역의 시작 페이지 번호
		"""
		result = self.get_page_no_at_cursor()
		return result

	def get_para_no_at_cursor(self):
		"""
		현재커서의 문단 번호
		"""
		result = self.han_program.GetPos()[1]
		#result = self.han_program.KeyIndicator()[4]  # 단
		return result

	def get_shape_object_by_no(self, input_no):
		"""
		그리기 개개체를 번호로 선택하기
		"""
		ctrl = self.han_program.HeadCtrl  # 첫번째 컨트롤(HaedCtrl)부터 탐색 시작.
		count = 0
		result = False

		while ctrl != None:
			nextctrl = ctrl.Next
			if ctrl.CtrlID == "gso":
				count += 1
				if input_no == count:
					self.han_program.SetPosBySet(ctrl.GetAnchorPos(0))
					self.han_program.FindCtrl()
					break
			ctrl = nextctrl
		return result

	def insert_left_line_at_end_of_table(self):
		"""
		테이블의 맨 왼쪽에 줄 삽입
		"""
		self.han_program.CreateAction("TableInsertLeftColumn")

	def insert_lower_line_at_end_of_table(self):
		"""
		테이블의 맨 아레쪽에 줄 삽입
		"""
		self.han_program.CreateAction("TableInsertLowerRow")

	def insert_multi_xline_in_table(self, input_no):
		"""
		테이블의 아래쪽에 여러줄 삽입
		"""
		for no in range(input_no):
			self.han_program.CreateAction("TableInsertLowerRow")

	def insert_next_line_at_cusor(self):
		self.han_program.HAction.Run("BreakPara")  # 줄바꾸기

	def insert_right_line_at_end_of_table(self):
		self.han_program.CreateAction("TableInsertRightColumn")

	def insert_table_x_line_at_cusor(self):
		"""
		테이블의 아래쪽에 한줄 삽입
		"""
		self.han_program.HAction.Run("TableInsertLowerRow") #줄추가

	def insert_upper_line_at_end_of_table(self):
		"""
		테이블의 위쪽에 한줄 삽입
		"""
		self.han_program.CreateAction("TableInsertUpperRow")

	def is_empty(self):
		return self.han_program.IsEmpty

	def is_modified(self) -> bool:
		return self.han_program.IsModified

	def is_selection(self):
		result = self.han_program.SelectionMode
		print("영역을 선택하였는가 ??", result)
		return result

	def make_table(self, x, y):
		self.han_program.HParameterSet.HTableCreation.Rows = x
		self.han_program.HParameterSet.HTableCreation.Cols = y
		self.han_program.HParameterSet.HTableCreation.WidthType = 2
		self.han_program.HParameterSet.HTableCreation.HeightType = 1
		self.han_program.HParameterSet.HTableCreation.WidthValue = self.han_program.MiliToHwpUnit(148.0)
		self.han_program.HParameterSet.HTableCreation.HeightValue = self.han_program.MiliToHwpUnit(150)
		self.han_program.HParameterSet.HTableCreation.CreateItemArray("ColWidth", x)
		self.han_program.HParameterSet.HTableCreation.CreateItemArray("RowHeight", y)
		self.han_program.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 1  # 글자처럼 취급
		self.han_program.HParameterSet.HTableCreation.TableProperties.Width = self.han_program.MiliToHwpUnit(148)
		self.han_program.HAction.Execute("TableCreate", self.han_program.HParameterSet.HTableCreation.HSet)


	def move_begin_cell_of_table(self):
		"""
		테이블의 처음으로 커서 옮기기
		"""
		self.han_program.HAction.Run("ShapeObjTableSelCell")

	def move_begin_of_xline_for_table(self):
		"""
		테이블의 가로줄의 처음르로 커서 옮기기
		"""
		self.han_program.HAction.Run("TableRowBegin")

	def move_begin_of_yline_for_table(self):
		"""
		테이블의 세로줄의 처음르로 커서 옮기기
		"""
		self.han_program.HAction.Run("TableColBegin")

	def move_cell_to_begin_of_xline_at_table(self):
		"""
		테이블의 가로줄의 처음르로 커서 옮기기
		"""
		return self.han_program.MovePos(moveID=104)

	def move_cell_to_begin_of_yline_at_table(self):
		"""
		테이블의 세로줄의 처음르로 커서 옮기기
		"""
		return self.han_program.MovePos(moveID=106)

	def move_cell_to_end_of_xline_at_table(self):
		"""
		테이블의 오른쪽으로 끝칸으로 커서 옮기기
		"""
		return self.han_program.MovePos(moveID=105)

	def move_cell_to_end_of_yline_at_table(self):
		"""
		테이블의 아래쪽으로 끝칸으로 커서 옮기기
		"""
		return self.han_program.MovePos(moveID=107)

	def move_cell_to_one_down_at_table(self):
		"""
		테이블의 아래로 한칸 커서 옮기기
		"""
		return self.han_program.MovePos(moveID=103)

	def move_cell_to_one_left_at_table(self):
		"""
		테이블의 왼쪽으로 한칸 커서 옮기기
		"""
		return self.han_program.MovePos(moveID=100)

	def move_cell_to_one_right_at_table(self):
		"""
		테이블의 오른쪽으로 한칸 커서 옮기기
		"""
		return self.han_program.MovePos(moveID=101)

	def move_cell_to_one_up_at_table(self):
		"""
		테이블의 한칸위로 커서 옮기기
		"""
		return self.han_program.MovePos(moveID=102)

	def move_cursor_by_filed_name(self, filed_name):
		"""
		필드이름으로 커서를 옮기기
		"""
		self.han_program.MoveToField(filed_name, True, True, True)

	def move_cursor_nth_char_from_current_para(self, input_no):
		"""
		현재 문단의 n번째 글자로 커서를 옮기기
		"""
		return self.han_program.MovePos(pos=input_no)

	def move_cursor_to_para_by_no(self, input_no):
		"""
		n번째 문단으로 커서를 옮기기
		"""
		return self.han_program.MovePos(Para=input_no)

	def move_cursor_to_begin_of_current_line(self):
		"""
		현재라인의 시작으로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=22)

	def move_cursor_to_begin_of_current_para(self):
		"""
		현재 문단의 시작으로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=6)

	def move_cursor_to_begin_of_current_word(self):
		"""
		현재 단어의 시작으로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=8)

	def move_cursor_to_begin_of_doc(self):
		"""
		현재 문서의 시작으로 커서를 옮기기
		"""
		self.han_program.MovePos(2)  # 문서 제일 앞으로
		#return self.han_program.MovePos(moveID=2)
		#self.han_program.HAction.Run("MoveDocBegin")

	def move_cursor_to_begin_of_line_no(self, input_no):
		"""
		줄번호의 위치로 커서를 옮기기
		"""
		self.move_cursor_to_begin_of_doc()
		self.move_cursor_to_nth_line_from_selection(input_no)

	def move_cursor_to_begin_of_next_para(self):
		self.han_program.MovePos(moveID=10)
		#self.han_program.HAction.Run("MoveNextParaBegin")

	def move_cursor_to_begin_of_selection(self):
		"""
		선택영역의 시작 위치로 커서를 옮기기
		"""
		self.han_program.HAction.Run("MoveListBegin")

	def move_cursor_to_end_of_selection(self):
		"""
		선택영역의 끝 위치로 커서를 옮기기
		"""
		self.han_program.HAction.Run("MoveListEnd")

	def move_cursor_to_end_of_current_line(self):
		"""
		현재 줄의 끝위치로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=23)

	def move_cursor_to_end_of_current_para(self):
		"""
		현재 문단의 끝위치로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=7)

	def move_cursor_to_end_of_current_word(self):
		"""
		현재 단어의 끝으로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=9)

	def move_cursor_to_end_of_doc(self):
		"""
		현재 문서의 끝위치로 커서를 옮기기
		"""
		self.han_program.MovePos(moveID=3)

	def move_cursor_to_end_of_previous_para(self):
		"""
		전 문단의 끝으로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=11)

	def move_cursor_to_end_of_range(self):
		"""
		영역의 끝으로 커서를 이동
		"""
		self.han_program.HAction.Run("MoveListEnd")

	def move_cursor_to_left_cell_of_table(self):
		"""
		테이블의 한칸 왼쪽셀로 커서를 옮기기
		"""
		self.han_program.HAction.Run("TableLeftCell")

	def move_cursor_to_next_char(self):
		"""
		한 글자뒤로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=12)

	def move_cursor_to_next_char_from_selection(self):
		"""
		선택영역에서 한글자 뒤로 커서를 옮기기
		"""
		self.han_program.HAction.Run("MoveNextChar")

	def move_cursor_to_next_line(self):
		"""
		선택영역에서 한줄 뒤로 커서를 옮기기
		"""
		#self.han_program.HAction.Run("MoveNextLine")
		return self.han_program.MovePos(moveID=20)

	def move_cursor_to_nth_char_from_selection(self, input_no):
		"""
		선택영역에서 n번째 글자 뒤로 커서를 옮기기
		"""
		if input_no > 0:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextChar")
		else:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextChar")

	def move_cursor_to_nth_line_from_selection(self, input_no):
		"""
		선택영역에서 n번째 줄뒤로 커서를 옮기기
		"""
		if input_no > 0:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextLine")
		else:
			for no in range(input_no):
				self.han_program.HAction.Run("MovePrevLine")

	def move_cursor_to_nth_para_from_selection(self, input_no):
		"""
		선택영역에서 n번째 문단 뒤로 커서를 옮기기
		"""
		position_obj = self.han_program.GetPos()
		self.han_program.SetPos(position_obj.list, position_obj.para +input_no, position_obj.pos)

	def move_cursor_to_nth_word_from_selection(self, input_no):
		"""
		선택영역에서 n번째 단어 뒤로 커서를 옮기기
		"""
		for no in range(input_no):
			self.han_program.HAction.Run("MoveNextWord")

	def move_cursor_to_nth_word_from_selection_old(self, input_no):
		if input_no > 0:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextWord")
		else:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextWord")

	def move_cursor_to_next_para_from_selection(self):
		"""
		선택영역에서 n번째 문단 뒤로 커서를 옮기기
		"""
		self.han_program.HAction.Run("MoveNextPara")

	def move_cursor_to_next_shape_object(self):
		"""
		다음 그리기객체로 커서이동
		"""
		return self.han_program.HAction.Run("ShapeObjNextObject")

	def move_cursor_to_next_word_from_selection(self):
		"""
		선택영역에서 다음 단어로 커서를 옮기기
		"""
		self.han_program.HAction.Run("MoveNextWord")

	def move_cursor_to_nth_char_from_begin_of_doc(self, input_no):
		"""
		문서의 n번째 글자로 커서를 옮기기
		"""
		self.move_cursor_to_begin_of_doc()
		self.move_cursor_to_nth_char_from_selection(input_no)

	def move_cursor_to_nth_line_from_begin_of_doc(self, input_no):
		"""
		문서의 n번째 줄로 커서를 옮기기
		"""
		self.move_cursor_to_begin_of_doc()
		for no in range(input_no):
			self.han_program.HAction.Run("MoveLineDown")

	def move_cursor_to_previous_char(self):
		"""
		바로전 글자로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=13)

	def move_cursor_to_previous_line(self):
		"""
		바로전 줄로 커서를 옮기기
		"""
		return self.han_program.MovePos(moveID=21)


	def move_cursor_to_previous_nth_word_from_selection(self, input_no):
		"""
		선택영역에서 n번째전 단어로 커서를 옮기기
		"""
		for no in range(input_no):
			self.han_program.HAction.Run("MovePrevWord")

	def move_cursor_to_previous_nth_char_from_selection(self, input_no):
		"""
		선택영역에서 n번째전 글자로 커서를 옮기기
		"""
		for no in range(input_no):
			self.han_program.MovePos(moveID=13)

	def move_cursor_to_previous_nth_line_from_selection(self, input_no):
		"""
		선택영역에서 n번째전 줄로 커서를 옮기기
		"""
		for no in range(input_no):
			self.han_program.MovePos(moveID=21)

	def move_cursor_to_previous_nth_para_from_selection(self, input_no):
		"""
		선택영역에서 n번째전 문단으로 커서를 옮기기
		"""
		if input_no > 0:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveUp")
		else:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveUp")

	def move_cursor_to_start_of_next_para(self):
		#다음 분단이 올때까지 이동
		self.han_program.HAction.Run("MoveParaEnd")

	def move_cursor_to_start_of_range(self):
		self.han_program.HAction.Run("MoveListBegin")

	def move_page(self):
		# 5페이지로 이동
		target_page = 5
		self.han_program.HAction.Run("MoveDocBegin") # 문서 시작으로 이동
		for _ in range(target_page-1):
			self.han_program.HAction.Run("MovePageDown") # 문서 시작으로 이동
		self.han_program.InitScan(...)

	def new_doc(self):
		"""
		새로운 문서 open
		"""
		self.han_program.XHwpDocuments.Add(0)

	def new_tab(self):
		"""
		새로운 탭만들기
		"""
		self.han_program.XHwpDocuments.Add(1)

	def new_table_at_cursor(self, x, y):
		"""
		새로운 테이블 만들기
		"""
		self.han_program.HParameterSet.HTableCreation.Rows = x
		self.han_program.HParameterSet.HTableCreation.Cols = y
		self.han_program.HParameterSet.HTableCreation.WidthType = 2
		self.han_program.HParameterSet.HTableCreation.HeightType = 1
		self.han_program.HParameterSet.HTableCreation.WidthValue = self.han_program.MiliToHwpUnit(148.0)
		self.han_program.HParameterSet.HTableCreation.HeightValue = self.han_program.MiliToHwpUnit(150)
		self.han_program.HParameterSet.HTableCreation.TableProperties.Width = self.han_program.MiliToHwpUnit(148)
		self.han_program.HAction.Execute("TableCreate", self.han_program.HParameterSet.HTableCreation.HSet)

	def page_break(self):
		"""
		페이지 바꾸기
		"""
		self.han_program.HAction.Run("BreakPage") #쪽나눔

	def paint_border_in_selection_with_pen(self):
		"""
		형광펜
		"""
		self.select_current_line()
		act = self.han_program.CreateAction("MarkPenShape")
		set = act.CreateSet()
		act.GetDefault(set)
		set.SetItem("Color", 65535)
		act.Execute(set)

	def paint_font_red_color_for_selection(self):
		"""
		선택영역을 빨간색으로 칠하기
		"""
		self.han_program.HAction.Run("CharShapeTextColorRed") #선택한 텍스트의 색을 빨간색으로 만든다

	def paint_table(self):
		"""
		테이블의 색을 칠하는 것
		"""
		act = self.han_program.CreateAction("CellFill")
		set = act.CreateSet()
		act.GetDefault(set)
		fillattrSet = set.CreateItemSet("FillAttr", "DrawFillAttr")

		fillattrSet.SetItem("Type", 1)
		fillattrSet.SetItem("WinBrushFaceStyle", 0xffffffff)
		fillattrSet.SetItem("WinBrushHatchColor", 0x00000000)
		fillattrSet.SetItem("WinBrushFaceColor", self.han_program.RGBColor(153, 153, 153))
		act.Execute(set)

	def quit(self):
		"""
		종료
		"""
		return self.han_program.Quit()

	def read_all_text_for_one_page(self, input_page_no):
		"""
		한페이지의 모든 text를 갖고온다
		"""
		return self.han_program.GetPageText(pgno=input_page_no)

	def read_text_for_current_line(self):
		self.select_current_line()
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def read_text_for_current_para(self):
		"""
		현재 문단의 text갖고오기
		"""
		self.move_cursor_to_begin_of_current_para()
		self.select_current_para()
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def read_text_for_para_no(self, input_no):
		"""
		문단번호로 text갖고오기
		"""
		self.move_cursor_to_begin_of_doc()
		self.select_nth_para_from_begin_of_doc(input_no)
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def read_text_from_index1_to_index2(self, input_no1, input_no2):
		"""
		글자번호 사이의 text갖고오기
		"""
		self.move_cursor_to_nth_char_from_begin_of_doc(input_no1)
		self.select_nth_char_from_selection(input_no2)
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def read_text_in_table_by_xy(self, table_object, x, y):
		"""
		테이블의 위치로 셀의 text갖고오기
		"""
		table_object.Run("ShapeObjTableSelCell")

		for no in range(y-1):
			table_object.Run("TableRightCell")

		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def read_value_in_selection(self):
		"""
		선택영역의 text갖고오기
		"""
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def rgb_color(self, red, green, blue):
		"""
		rgb값
		"""
		return self.han_program.RGBColor(red=red, green=green, blue=blue)

	def save(self, file_name=""):
		"""
		저장
		"""
		self.han_program.SaveAs(file_name)
		self.han_program.Quit()

	def select_first_cell_of_table(self, table_no):
		"""
		테이블의 처음 셀을 선택
		"""
		self.select_table_object_by_no(table_no)
		self.han_program.Run("ShapeObjTableSelCell")

	def select_all(self):
		"""
		문서의 모든 것을 선택
		"""
		self.han_program.Run('SelectAll')

	def select_current_line(self):
		"""
		현재 줄을 선택
		"""
		self.han_program.HAction.Run("MoveSelLineEnd")
		#self.han_program.Run("Select")
		#self.han_program.HAction.Run("MoveLineEnd")

	def select_current_para(self):
		"""
		현재 문단 선택
		"""
		self.han_program.HAction.Run("MoveParaBegin")
		self.han_program.Run("Select")
		self.han_program.HAction.Run("MoveParaEnd")

	def select_current_word(self):
		"""
		현재 단어 선택
		"""
		self.han_program.HAction.Run("MoveWordBegin")
		self.han_program.Run("Select")
		self.han_program.HAction.Run("MoveWordEnd")

	def select_end_of_line_from_selection(self):
		"""
		현재 선택영역에서 줄의 끝까지 선택
		"""
		self.han_program.HAction.Run("MoveSelLineEnd")

	def select_end_of_para_from_selection(self):
		"""
		현재 선택영역에서 문단의 끝까지 선택
		"""
		self.han_program.HAction.Run("MoveSelParaEnd")

	def select_from_begin_of_doc_to_nth_char(self, input_no):
		"""
		문서의 시작에서부터 n번째 글짜까지 선택
		"""
		self.select_nth_char_from_begin_of_doc(input_no)

	def select_from_begin_of_doc_to_nth_line(self, input_no):
		"""
		문서의 시작에서부터 n번째 줄까지 선택
		"""
		self.han_program.Run("Select")
		for no in range(input_no):
			self.han_program.HAction.Run("MoveNextLine")
		self.han_program.HAction.Run("MoveSelLineEnd")

	def select_from_begin_of_doc_to_nth_para(self, input_no):
		"""
		문서의 시작에서부터 n번째 문단까지 선택
		"""
		self.select_nth_para_from_selection(input_no)

	def select_from_begin_of_doc_to_nth_word(self, input_no):
		"""
		문서의 시작에서부터 n번째 단어까지 선택
		"""
		self.select_nth_word_from_begin_of_doc(input_no)

	def select_from_char_no1_to_no2_from_begin_of_doc(self, input_no1, input_no2):
		"""
		두 글자번호 사이를 선택
		"""
		self.move_cursor_to_nth_char_from_begin_of_doc(input_no1)
		self.select_nth_char_from_selection(input_no2 - input_no1)

	def select_from_cursor_to_nth_char(self, input_no):
		"""
		현재커서에서 n번째 글자까지 선택
		"""
		self.select_nth_char_from_selection(input_no)

	def select_from_cursor_to_nth_word(self, input_no):
		"""
		현재커서에서 n번째 단어까지 선택
		"""
		self.select_nth_word_from_selection(input_no)

	def select_from_cursor_to_previous_nth_char(self, input_no):
		"""
		현재커서에서 n번째 앞의 글자까지 선택
		"""
		for one in range(input_no):
			self.move_cursor_to_previous_char()

	def select_from_cursor_to_previous_nth_word(self, input_no):
		"""
		현재커서에서 n번째 앞의 단어까지 선택
		"""
		self.move_cursor_to_previous_nth_word_from_selection(input_no)
		self.select_current_word()

	def select_from_line_no1_to_no2_from_selection(self, input_no1, input_no2):
		"""
		두 줄사이를 선택
		"""
		self.move_cursor_to_nth_line_from_selection(input_no1)
		self.select_nth_line_from_selection(input_no2-input_no1)

	def select_from_para_no1_to_no2_from_selection(self, input_no1, input_no2):
		"""
		두 문단사이를 선택
		"""
		self.select_nth_para_from_selection(input_no2-input_no1)

	def select_line_by_no(self, input_no):
		"""
		줄번호로 선택
		"""
		#self.move_cursor_to_begin_of_doc()
		self.move_cursor_to_nth_line_from_begin_of_doc(input_no-1)
		self.select_current_line()

	def select_nth_char_from_selection(self, input_no):
		"""
		선택영역에서 n번째 글짜까지 선택
		"""
		#self.move_cursor_to_begin_of_doc()
		self.move_cursor_to_nth_char_from_selection(input_no)
		#self.han_program.Run("Select")
		#self.han_program.SetPos(position_obj.list, position_obj.para, position_obj.pos +input_no)

	def select_nth_line_from_cursor(self, input_no):
		"""
		선택영역에서 n번째 줄까지 선택
		"""
		for no in range(input_no):
			self.han_program.HAction.Run("MoveSelNextLine")

	def select_nth_line_from_selection(self, input_no):
		"""
		선택영역에서 n번째 글짜까지 선택
		"""
		for no in range(input_no):
			self.han_program.HAction.Run("MoveSelNextLine")

	def select_nth_para_from_selection(self, input_no):
		"""
		선택영역에서 n번째 문단을 선택
		"""
		self.move_cursor_to_nth_para_from_selection(input_no)
		#self.han_program.Run("Select")
		self.select_current_para()
		#self.han_program.SetPos(position_obj.list, position_obj.para +input_no, position_obj.pos)

	def select_nth_word_from_selection(self, input_no):
		"""
		선택영역에서 n번째 단어를 선택
		"""
		for no in range(input_no):
			self.han_program.HAction.Run("MoveSelNextWord")

	def select_next_char_from_selection(self, input_no):
		"""
		선택영역에서 n번째 글짜를 선택
		"""
		self.move_cursor_to_nth_char_from_selection(1)

	def select_next_para_from_selection(self):
		"""
		선택영역에서 n번째 문단을 선택
		"""
		self.move_cursor_to_next_para_from_selection()
		self.select_current_para()

	def select_next_word_from_selection(self):
		"""
		선택영역에서 n번째 단어을 선택
		"""
		self.select_nth_word_from_selection(1)

	def select_next_line_from_selection(self):
		"""
		선택영역에서 다음 줄을 선택
		"""
		self.han_program.HAction.Run("MoveSelNextLine")

	def select_nth_char_from_begin_of_doc(self,input_no):
		"""
		n번째 글자를 선택
		"""
		self.move_cursor_to_nth_char_from_begin_of_doc(input_no)

	def select_nth_line_from_begin_of_doc(self, input_no):
		"""
		n번째 줄을 선택
		"""
		self.move_cursor_to_nth_line_from_begin_of_doc(input_no)
		self.select_current_line()

	def select_nth_para_from_begin_of_doc(self, input_no):
		"""
		n번째 문단을 선택
		"""
		self.move_cursor_to_para_by_no(input_no)
		self.select_current_para()

	def select_nth_word_from_begin_of_doc(self, input_no):
		"""
		n번째 단어를 선택
		"""
		self.select_nth_word_from_begin_of_doc(input_no)

	def select_previous_char_from_selection(self):
		"""
		선택영역에서 앞으로 n번째 글자를 선택
		"""
		self.han_program.HAction.Run("MoveSelPrevPos")

	def select_previous_nth_line_from_selection(self, input_no):
		"""
		선택영역에서 앞으로 n번째 줄을 선택
		"""
		for no in range(input_no):
			self.han_program.HAction.Run("MovePrevLine")

	def select_previous_nth_para_from_selection(self):
		"""
		선택영역에서 앞으로 n번째 문단을 선택
		"""
		self.move_cursor_to_previous_nth_para_from_selection(1)
		self.select_current_para()

	def select_previous_nth_word_from_selection(self):
		"""
		선택영역에서 앞으로 n번째 단어를 선택
		"""
		self.move_cursor_to_previous_nth_word_from_selection(1)
		self.select_current_word()

	def select_previous_word_from_selection(self):
		"""
		선택영역에서 앞 단어를 선택
		"""
		self.han_program.HAction.Run("MoveSelPrevWord")

	def select_previous_line_from_selection(self):
		"""
		선택영역에서 앞 줄을 선택
		"""
		self.han_program.HAction.Run("MoveSelLineUp")

	def select_previous_para_from_selection(self):
		"""
		선택영역에서 앞 문단을 선택
		"""
		self.han_program.HAction.Run("MovePrevPara")
		self.han_program.HAction.Run("MoveParaBegin")
		self.han_program.Run("Select")
		self.han_program.HAction.Run("MoveParaEnd")

	def select_start(self):
		"""
		선택 시작
		"""
		self.han_program.HAction.Run("Select")

	def select_start_of_line_from_selection(self):
		"""
		선택영역의 첫번째 라인을 선택
		"""
		self.han_program.HAction.Run('MoveSelLineBegin')

	def select_start_of_list_from_selection(self):
		"""
		선택영역의 리스트의 시작 번호
		"""
		self.han_program.HAction.Run('MoveSelListBegin')

	def select_start_of_para_from_selection(self):
		"""
		선택영역의 첫번째 문단을 선택
		"""
		self.han_program.HAction.Run("MoveSelParaBegin")

	def select_start_of_word_from_selection(self):
		"""
		선택영역의 첫번째 단어를 선택
		"""
		self.han_program.HAction.Run("MoveSelWordEnd")

	def select_table_object_by_no(self, input_no):
		#한글에서는 객체를 넘겨주는 부분이 아니고
		#원하는 객체를 문서 젠체에서 사용가능한 선택을 하고, 다른곳에서 선택한것을 가지고 무엇인가 한다
		ctrl = self.han_program.HeadCtrl  # 첫번째 컨트롤(HaedCtrl)부터 탐색 시작.
		count = 0
		while ctrl != None:
			nextctrl = ctrl.Next
			print(ctrl.CtrlID)
			if ctrl.CtrlID == "tbl":
				count += 1
				if input_no == count:
					print(count)
					self.han_program.SetPosBySet(ctrl.GetAnchorPos(0))
					self.han_program.FindCtrl()
					break
			ctrl = nextctrl

	def select_xline_in_table(self):
		"""
		가로줄 선택
		"""
		self.han_program.CreateAction("Select")

	def select_yline_in_table(self, table_no, y):
		"""
		세로줄 선택
		"""
		self.select_table_object_by_no(table_no)
		self.han_program.Run("ShapeObjTableSelCell")
		for no in range(y-1):
			self.han_program.Run("TableRightCell")
		self.han_program.CreateAction("SelectColumn")

	def selection_value(self):
		"""
		선택영역의 텍스트
		"""
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def set_alignment_left_for_para(self):
		"""
		왼쪽 정렬
		"""
		self.han_program.HAction.Run("ParagraphShapeAlignLeft")

	def set_cur_field_name(self, field_name):
		#현재 캐럿이 있는 곳의 필드이름을 설정
		return self.han_program.SetCurFieldName(Field=field_name)

	def set_font_bold_in_selection(self):
		self.han_program.HAction.Run("CharShapeBold")  # 진하게 적용

	def set_font_alignment_left_in_selection(self):
		"""
		왼쪽 정렬
		"""
		self.han_program.HAction.Run("ParagraphShapeAlignLeft")

	def set_font_alignment_right_in_selection(self):
		"""
		오른쪽 정렬
		"""
		self.han_program.HAction.Run("ParagraphShapeAlignRight")

	def set_font_alignment_center_in_selection(self):
		"""
		가운데 정렬
		"""
		self.han_program.HAction.Run("ParagraphShapeAlignCenter")

	def paint_highlight_for_selection(self):
		"""
		형광펜
		"""
		self.select_current_line()
		act = self.han_program.CreateAction("MarkPenShape")
		set = act.CreateSet()
		act.GetDefault(set)
		set.SetItem("Color", 65535)
		act.Execute(set)

	def set_font_shadow_in_selection(self):
		"""
		그림자
		"""
		self.han_program.HAction.Run("CharShapeShadow")

	def set_font_size_up_in_selection(self):
		"""
		폰트크기 1단계 키우기
		"""
		self.han_program.HAction.Run("CharShapeHeightIncrease")

	def set_font_size_down_in_selection(self):
		"""
		폰트크기 1단계 줄이기
		"""
		self.han_program.HAction.Run("CharShapeHeightDecrease")

	def set_font_color_as_red_in_selection(self):
		"""
		글자를 빨간색으로 색칠하기
		"""
		self.han_program.HAction.Run("CharShapeTextColorRed") #선택한 텍스트의 색을 빨간색으로 만든다

	def set_font_color_in_selection_by_rgb(self, input_rgb):
		"""
		선택영역 rgb값으로 색칠하기
		"""
		rgb_value = self.han_program.RGBColor(red=input_rgb[0], green=input_rgb[1], blue=input_rgb[2])
		act = self.han_program.CreateAction("CharShape")
		cs = act.CreateSet()
		act.GetDefault(cs)
		cs.SetItem("TextColor", rgb_value)
		act.Execute(cs)

	def set_font_color_in_selection_by_scolor(self, input_scolor):
		"""
		선택영역 scolor형식으로 색칠하기
		"""
		input_rgb = self.color.change_scolor_to_rgb(input_scolor)
		rgb_value = self.han_program.RGBColor(red=input_rgb[0], green=input_rgb[1], blue=input_rgb[2])
		act = self.han_program.CreateAction("CharShape")
		cs = act.CreateSet()
		act.GetDefault(cs)
		cs.SetItem("TextColor", rgb_value)
		act.Execute(cs)

	def set_table_cell_address(self, addr):
		"""
		셀번호를 a1형태로 돌려준다
		"""
		init_addr = self.han_program.KeyIndicator()[-1][1:].split(")")[0]  # 함수를 실행할 때의 주소를 기억.
		if not self.han_program.CellShape:  # 표 안에 있을 때만 CellShape 오브젝트를 리턴함
			raise AttributeError("현재 캐럿이 표 안에 있지 않습니다.")
		if addr == self.han_program.KeyIndicator()[-1][1:].split(")")[0]:  # 시작하자 마자 해당 주소라면
			return  # 바로 종료
		self.han_program.HAction.Run("CloseEx")  # 그렇지 않다면 표 밖으로 나가서
		self.han_program.FindCtrl()  # 표를 선택한 후
		self.han_program.HAction.Run("ShapeObjTableSelCell")  # 표의 첫 번째 셀로 이동함(A1으로 이동하는 확실한 방법 & 셀선택모드)
		while True:
			current_addr = self.han_program.KeyIndicator()[-1][1:].split(")")[0]  # 현재 주소를 기억해둠
			self.han_program.HAction.Run("TableRightCell")  # 우측으로 한 칸 이동(우측끝일 때는 아래 행 첫 번째 열로)
			if current_addr == self.han_program.KeyIndicator()[-1][1:].split(")")[0]:  # 이동했는데 주소가 바뀌지 않으면?(표 끝 도착)
				# == 한 바퀴 돌았는데도 목표 셀주소가 안 나타났다면?(== addr이 표 범위를 벗어난 경우일 것)
				self.set_table_cell_address(init_addr)  # 최초에 저장해둔 init_addr로 돌려놓고
				self.han_program.HAction.Run("Cancel")  # 선택모드 해제
				raise AttributeError("입력한 셀주소가 현재 표의 범위를 벗어납니다.")
			if addr == self.han_program.KeyIndicator()[-1][1:].split(")")[0]:  # 목표 셀주소에 도착했다면?
				return  # 함수 종료

	def write_text_at_begin_of_line_no(self, input_no):
		"""
		줄번호의 시작에 텍스트입력
		"""
		self.move_cursor_to_begin_of_doc()
		self.move_cursor_to_nth_line_from_begin_of_doc(input_no)
		self.move_cursor_to_begin_of_current_line()
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def write_text_at_begin_of_selection(self):
		"""
		선택영역 시작에 텍스트입력
		"""
		self.move_cursor_to_begin_of_selection()
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def write_text_at_cursor(self, input_value):
		"""
		커서위치에 텍스트입력
		"""
		changed_text = input_value.split("\n")
		print(len(changed_text))
		for one_text in changed_text:
			action = self.han_program.CreateAction("InsertText")
			pset = action.CreateSet()
			pset.SetItem("Text", one_text)
			action.Execute(pset)
			self.han_program.Run("BreakLine")


	def write_text_at_end_of_doc(self, input_text):
		"""
		문서의 끝에 텍스트입력
		"""
		self.move_cursor_to_end_of_doc()
		self.han_program.SetTextFile(input_text, "TEXT", "insertfile")

	def write_text_at_end_of_selection(self, input_text):
		"""
		선택영역의 끝에 텍스트입력
		"""
		self.move_cursor_to_end_of_selection()
		self.han_program.SetTextFile(input_text, "TEXT", "insertfile")

	def write_text_at_start_of_selection(self, input_text):
		"""
		선택영역의 처음에 텍스트입력
		"""
		self.move_cursor_to_begin_of_selection()
		self.han_program.SetTextFile(input_text, "TEXT", "insertfile")

	def write_text_at_nth_cell_in_table(self, table_no, y, input_text):
		"""
		테이블의 순번째에 텍스트입력
		"""
		self.select_table_object_by_no(table_no)
		self.han_program.Run("ShapeObjTableSelCell")
		for no in range(y-1):
			self.han_program.Run("TableRightCell")

		self.han_program.SetTextFile(input_text, "TEXT", "insertfile")

	def write_text_in_table_by_xy(self, table_no, x, y, input_text):
		"""
		선택영역의 처음에 텍스트입력
		"""
		self.select_table_object_by_no(table_no)
		self.han_program.Run("ShapeObjTableSelCell")
		for no in range(x-1):
			self.han_program.Run("TableLowerCell")

		for no in range(y-1):
			self.han_program.Run("TableRightCell")
		self.write_text_at_cursor(input_text)

	def write_text_with_new_line_at_end_of_doc(self, input_text):
		"""
		문서의 끝에 새로운 라인으로 텍스트입력
		"""
		self.move_cursor_to_end_of_doc()
		self.insert_next_line_at_cusor()
		self.han_program.SetTextFile(input_text, "TEXT", "insertfile")

	def write_value_at_end_of_para_no(self, input_text):
		"""
		특정 문단의 끝에 텍스트입력
		"""
		self.move_cursor_to_end_of_current_para()
		self.han_program.SetTextFile(input_text, "TEXT", "insertfile")

