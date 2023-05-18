import time
from zk import ZK, const
from erpnext.accounts.doctype.employee.employee import Employee
from erpnext.hr.doctype.attendance.attendance import Attendance

# Connect to the device
zk = ZK('10.10.0.4', port=4370, timeout=5)
conn = zk.connect()

# Set the device to push mode
zk.set_push()

# Get attendance data
attendance = zk.get_attendance()

# Loop through attendance data and push to ERPNext
for att in attendance:
    # Retrieve employee details from ERPNext
    employee = Employee.get(att.user_id)
    
    # Format attendance date and time
    att_date = time.strftime('%Y-%m-%d', time.localtime(att.timestamp))
    att_time = time.strftime('%H:%M:%S', time.localtime(att.timestamp))
    
    # Create attendance record in ERPNext
    attendance = Attendance(attendance_date=att_date, employee=employee.name, employee_name=employee.employee_name, company=employee.company, status='Present', attendance_status='Present', attendance_time=att_time)
    attendance.insert(ignore_permissions=True)

# Disconnect from the device
zk.disconnect()