import matplotlib.pyplot as plt
import sqlite3
import numpy as np
import datetime as dt
import matplotlib.patches as mpatches
from phone_data import *
import subprocess
import sys


conn = sqlite3.connect('phone.db')
#rundate = dt.datetime.strptime('2016-06-20', '%Y-%m-%d')

if len( sys.argv ) > 1:
	try:
		rundate = dt.datetime(year=int(sys.argv[1]),month=int(sys.argv[2]), day=int(sys.argv[3]) )
	except (TypeError, ValueError):
		sys.exit("To Specify Start date Override, use syntax: python" + sys.argv[0] + " YYYY MM DD")
else:
	rundate = dt.datetime.strptime(get_newest_date(conn)[0][0], '%Y-%m-%d')


def plot_day(conn,rundate):
    cur = conn.cursor()
    plt.ioff()
 
    agent_info = get_agents(conn, [1, 2])
    agent_ids = [x[2] for x in agent_info]
    name_id = dict([(row[1], row[2]) for row in agent_info])

    cur.execute("select substr(firstname, 1,1) || '' || substr(upper(lastname), 1,3) Agent,\
                case when 3 in (select queue_id from stats_daily where date = ? and agent_id = sd.agent_id ) then 2 else 1 end Tier,\
                sum(ACD_CALLS) Total_Calls ,\
                sum( case when queue_id = 1 then ACD_CALLS else 0 end ) ANet,\
                sum( case when queue_id = 2 then ACD_CALLS else 0 end ) YMCA,\
                sum( case when queue_id = 4 then ACD_CALLS else 0 end ) Emerg,\
                sum( case when queue_id = 3 then ACD_CALLS else 0 end ) Tier2\
                from stats_daily sd join agents a on sd.AGENT_ID = a.agent_id \
                where date =  ? and acd_calls > 0  group by 1  order by 2,1", [rundate.strftime('%Y-%m-%d'),rundate.strftime('%Y-%m-%d')])
    rdata = cur.fetchall()
    if len(rdata) == 0:
        return -1
    agents = [x[0] for x in rdata]
    calls = np.array([int(x[2]) for x in rdata])
    anet = np.array([int(x[3]) for x in rdata])
    ymca = np.array([int(x[4]) for x in rdata])
    emerg = np.array([int(x[5]) for x in rdata])
    tier2 = np.array([int(x[6]) for x in rdata])

    hashstyles = ['/', '\\', '//']
    fig, ax = plt.subplots()
    fig.set_size_inches(9,6)
    fig.set_dpi(100)

    xticks = [i for i in range(1,len(calls) +1)]
    yticks = np.arange(0,max(calls),2)
    yticks = np.append(yticks,[max(yticks) + 2])


    ax.set_ylabel('Answered Calls')
    ax.set_title(rundate.strftime("%A, %b %d, '%y") + ' - ' + str(sum(anet) + sum(ymca) + sum(emerg)) + ' Inbound Calls Answered')

    s1 = ax.bar(xticks, tier2,  label='Tier2 - ' + str(sum(tier2)), linewidth=1.0, color  = '#8939FD', edgecolor='black')
    s2 = ax.bar(xticks, anet,  label='ANet - '+ str(sum(anet)), linewidth=1.0, color  = '#0054CE',bottom = tier2,  edgecolor='black', hatch = '')
    s3 = ax.bar(xticks, ymca,  label='YMCA - '+ str(sum(ymca)), color  = '#52E0E5', bottom = anet + tier2,  edgecolor='black', hatch = '')
    s4 = ax.bar(xticks, emerg,  label='Emerg - '+ str(sum(emerg)), color  = '#DA0000', bottom = ymca + anet + tier2, edgecolor='black')

    ax.set_xticks(xticks)
    ax.set_xticklabels(agents)

    ax.set_yticks(yticks)
    #ax.set_yticks([])

    ax.set_ylim([0,max(calls) + 2])

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., height + .11,
                    '%d' % int(height),
                    ha='center', va='bottom')

    def label_stacked(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect, h in zip(rects,calls):
            #height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., h + .11,
                    '%d' % int(h),
                    ha='center', va='bottom')

    def label_anet(rects):
        """
        Attach a text label above each bar displaying its height
        """

        for rect, h, j, k, l in zip(rects,anet, tier2, ymca, emerg):
            if (j == 0 and k == 0 and l == 0) or h == 0:
                continue
            height = h + j
            ax.text(rect.get_x() + rect.get_width()/2., height - 1.2,
                    '%d' % int(h),
                    ha='center', va='bottom', color = '#E1E1E1')

    label_stacked(s4)
    label_anet(s1)
    plt.legend()
    #plt.show()
    plt.savefig('Archive\\summary_' + rundate.strftime('%Y-%m-%d') + '.png', bbox_inches='tight')
    plt.savefig('daily_calls.png', bbox_inches='tight')
    plt.clf()
    with open('date.txt', 'w') as file:
        file.write("Daily Calls - " + rundate.strftime("%A %b %d, '%y"))

    return 0
enddate = dt.datetime.today()
while rundate < enddate:

    plot_day(conn,rundate)
    rundate = rundate + dt.timedelta(days=1)