def PrintToCSVReport(ReportFile,Data1,Append_write):
	# Append_write = 'x' if you want to create and write to the file
	# Append_write = 'a' if you want to append to the file
    ReportFiletemp = open(ReportFile, Append_write)
    ReportFiletemp.write(Data1 + '\n')
    ReportFiletemp.close()

