#!/usr/bin/env python
from shlex import split
from Clict import Clict
from textwrap import shorten
from subprocess import run,getoutput

def ls_blk(**k):
	cmd='lsblk --list --noheadings --nodeps --bytes --include 259,8 --output ALIGNMENT,ID-LINK,ID,DISC-ALN,DAX,DISC-GRAN,DISK-SEQ,DISC-MAX,DISC-ZERO,FSAVAIL,FSROOTS,FSSIZE,FSTYPE,FSUSED,FSUSE%,FSVER,GROUP,HCTL,HOTPLUG,KNAME,LABEL,LOG-SEC,MAJ:MIN,MIN-IO,MODE,MODEL,MQ,NAME,OPT-IO,OWNER,PARTFLAGS,PARTLABEL,PARTN,PARTTYPE,PARTTYPENAME,PARTUUID,PATH,PHY-SEC,PKNAME,PTTYPE,PTUUID,RA,RAND,REV,RM,RO,ROTA,RQ-SIZE,SCHED,SERIAL,SIZE,START,STATE,SUBSYSTEMS,MOUNTPOINT,MOUNTPOINTS,TRAN,TYPE,UUID,VENDOR,WSAME,WWN,ZONED,ZONE-SZ,ZONE-WGRAN,ZONE-APP,ZONE-NR,ZONE-OMAX,ZONE-AMAX'
	cmd=split(cmd)
	table= run(cmd,capture_output=True,text=True,universal_newlines=True)
	print('\n'.join(table.stdout.splitlines()))

def ls_blkdisks(**k) -> dict:
	"""
			:return: list of storage devices
			"""
	cmd_opts='--include 259,8 --nodeps -o NAME'#259 = maj:NVME , 8 =maj:scsi/sata
	return ls_blk(opts=cmd_opts).stdout.splitlines()

def ls_blkparts(**k):
	cmd_args_disk='/dev/{}'.format(k.get('disk')) if k.get('disk') else ''
	cmd_opts=f'-o TYPE,NAME {cmd_args_disk}'
	lst_stdout=ls_blk(opts=cmd_opts).stdout.splitlines()
	parts=[line.split()[1] for line in lst_stdout if line.split()[0]=='part']
	return parts

# def ls_blkfs(**k):
# 	rex=re.compile('\s*([a-zA-Z0-9]*?)$')
# 	partsfs=allfsparts=[]
# 	cmd_args_disk='/dev/{}'.format(k.get('disk')) if k.get('disk') else ''
# 	cmd_opts=f'--sort FSTYPE -o NAME,FSTYPE {cmd_args_disk}'
# 	lst_stdout=ls_blk(opts=cmd_opts).stdout.splitlines()
# 	partsfs= [line.split()[0] for line in lst_stdout if str(rex.search(line)[1]) == k.get('fs')]
# 	allfsparts=[line for line in lst_stdout if str(rex.search(line)[1])]
# 	return partsfs if k.get('fs') else allfsparts
#
#
#
#
#
#
# def ls_fs_btrfs():
# 	sys_btrfs='/sys/fs/btrfs/'
# 	if os.path.isdir(sys_btrfs):
# 		btrfs_vols=ls_dirs(sys_btrfs)
# 		btrfs_vols= [os.path.join(sys_btrfs,vol) for vol in btrfs_vols if vol!= os.path.join(sys_btrfs,'features')]
# 		btrfs_devs=[]
# 		for vol in btrfs_vols:
# 			devices=[os.path.split(dev)[1] for dev in  ls_dirs(os.path.join(vol,'devices'))]
# 			if os.path.isfile(os.path.join(vol,'label')):
# 				with open(os.path.join(vol,'label'),'r') as label:
# 					label=label.read().strip()
# 			else:
# 				label='!!NOLABEL!!'
# 			dev=[label,os.path.split(vol)[1],devices]
# 			btrfs_devs+=[dev]
# 	return btrfs_devs
# def main():
# 	ls_blk()
# if __name__ == '__main__':
# 	main()

#
print('\n\n\n\n')
from Clict import Clict
import os
BD=Clict()
term = Clict()
term.size = [*os.get_terminal_size()]
term.size[0] = term.size[0]
def toB(f, u):
	s = ' KMGTPEZYRQ'.index(u[0])
	b,p,Si = [10,3,False]
	if len(u)==3 and u[-1] == 'B':
		u=u[:-1]
	if len(u)==2:
		if u[-1]=='i':
			b,p,Si=[2,10,True]
	return int(float(f)*(b**(s*p)))
# def add_unallocated(start,stop):

def add_part(line,sectorcounter):
	pttcmd= run(split(f'sgdisk -I /dev/{DEV}'),capture_output=True,text=True,universal_newlines=True)

	part=Clict()
	il0 = int(line[0])
	if int(line[1]) != sectorcounter:
		add_unallocated(sectorcounter, line[1])

	part[il0].sector.start = int(line[1])
	part[il0].sector.end = int(line[2])
	part[il0].char.start = (int(line[1]) * (term.size[0]) - waste) // sectors
	part[il0].char.end = (int(line[2]) * (term.size[0]) - waste) // sectors
	part[il0].size.bytes = toB(int(float(line[3])), line[4])
	part[il0].size.sectors = disk.part[il0].sector.end - disk.part[il0].sector.start
	part[il0].size.chars = (3 + ((disk.part[il0].sector.end - disk.part[il0].sector.start) * ((term.size[0]) - waste)) // sectors)
	part[il0].str.top = '┌' + ('─' * (disk.part[il0].size.chars - 2)) + '┐'
	part[il0].str.mid = '│' + (' ' * (disk.part[il0].size.chars - 2)) + '│'
	part[il0].str.bot = '└' + ('─' * (disk.part[il0].size.chars - 2)) + '┘'
	part[il0].type.short = line[5]
	part[il0].PARTLABEL = ' '.join(line[6:]) if len(line) >= 7 else 'NONE'
def gptdrive(disk):
	partprog = "sgdisk -p {DRIVE}"
	result = run(split(partprog.format(DRIVE=f'/dev/{DEV}')), capture_output=True, text=True,
				 universal_newlines=True)
	rlines = result.stdout.splitlines()
	sectors = int(rlines[0].split()[2])
	onechar = sectors // (term.size[0] - 2)
	# print(onechar)
	parts = Clict()
	for n, line in enumerate(rlines):
		if line.casefold().startswith('number'):
			parts = [l.split() for l in rlines[n + 1:]]
			break
	# print(parts)

	startsector=40
	sectorcounter=startsector
	for n,line in enumerate(parts):
		waste = (n * 3) + 2
		# print(line)
		add_part(line,sectorcounter,)

	# print(disk.part[il0].PARTLABEL, il0)
	# print(disk.part[il0])
	return disk


def draw_drive(dev,term):
	pttcmd= run(split(f'lsblk --noheadings --nodeps --bytes -o PTTYPE /dev/{DEV}'),capture_output=True,text=True,universal_newlines=True)
	ptt=pttcmd.stdout.strip()
	# print(ptt)

	disk=Clict()
	disk.partitions
	if ptt=='gpt':
		disk=gptdrive(disk)



	sizes=[]
	sss=[]
	for part in disk.part:
		sizes+=[disk.part[part].size.chars]
		sss+=[(disk.part[part].char.start,disk.part[part].char.end)]
		# parts._0.sectors=

	def draw_rectangles(sizes):
		blocksizes=[]
		# Constants for box drawing characters
		BD.HOR.l = '─'
		BD.HOR.h = '━'
		BD.VER.l = '│'
		BD.VER.h = '┃'
		BD.TOP.L.l = '┌'
		BD.TOP.L.h = '┏'
		BD.TOP.R.l = '┐'
		BD.TOP.R.h = '┓'
		BD.BOT.L.l = '└'
		BD.BOT.L.h = '┗'
		BD.BOT.R.l = '┘'
		BD.BOT.R.h = '┛'
		BD.VERTICAL_SEPARATOR = '│'
		BD.HORIZONTAL_SEPARATOR = '┼'
		BD.MIDDLE_LEFT_LIGHT = '├'
		BD.MIDDLE_RIGHT_LIGHT = '┤'

		# Calculating the total width of the inner rectangles
		# inner_width = sum(sizes) + len(sizes) - 1
		# Full box width is fixed to 20 characters
		# full_box_width = term.size[0]

		# if inner_width > full_box_width - 2:
		# 	raise ValueError("The total width of inner rectangles exceeds the allowed width")
		drive=Clict
		# Drawing the heavy box border
		# lpad=1
		drive.top='{TLH}{HHPRE}|{DEV}|{HHPOST}{TRH}'.format(
					TLH=BD.TOP.L.h,
					HHPRE=BD.HOR.h*2,
					DEV=DEV,
					HHPOST=BD.HOR.h*(term.size[0]-6-len(DEV)),
					TRH=BD.TOP.R.h)
		drive.bot='{BLH}{HH}{BRH}'.format(
			BLH=BD.BOT.L.h,
			HH=BD.HOR.h*(term.size[0] - 2),
			BRH=BD.BOT.R.h)
		# Drawing the inner boxes top border
		top_parts_border=''
		bot_parts_border=''
		content=''
		for idx,size in enumerate(sizes):
		# 	parts_inner_top_border = BD.TOP.L.l + BD.HOR.l * (size - 2) + BD.TOP.R.l
			top_parts_border+=disk.part[idx+1].str.top
			bot_parts_border+=disk.part[idx+1].str.bot
			# content+=BD.VER.l+ shorten(f"{idx + 1}:{disk.part[idx+1].PARTLABEL}",size-2,placeholder='').ljust(size - 2)+ BD.VER.l
			# content+=BD.VER.l+ shorten(f"{idx + 1}:{disk.part[idx+1].PARTLABEL}",size-2,placeholder='').ljust(size - 2)+ BD.VER.l
			content+=disk.part[idx+1].str.mid
			inner_top_border = '{VH}{PTT}{PARTS}\x1b[{LAST}G{VH}'.format(VH=BD.VER.h,PTT='G',PARTS=top_parts_border,LAST=term.size[0])
			inner_content = '{VH}{PTT}{PARTS}\x1b[{LAST}G{VH}'.format(VH= BD.VER.h ,PTT='P',PARTS=content,LAST=term.size[0])

		inner_bot_border = '{VH}{PTT}{PARTS}\x1b[{LAST}G{VH}'.format(VH=BD.VER.h,PTT='T',PARTS=bot_parts_border,LAST=term.size[0])
		# print(drive.top)
		# print(inner_top_border)
		print(inner_content)
		# print(inner_bot_border)
		# print(drive.bot)
		# for part,(start,stop) in enumerate(sss):
		# 	# print(f'\x1b[{start+(3*(idx+1))}G└',end='')
		# 	print(f'\x1b[{start+1+(3*idx)}G{start}',end='')


			# arr[x]= '└','-','┘'

		# return arr
	row=[*' '*term.size[0]]
	# print(row)
	offset=3
	for idx,ss in enumerate(sss):
		offset+=idx*3
		# row=fliparray(row,ss)
		# loc=minoff

	# print(''.join(row))
			#
			# print(f'\x1b[{stop-1}G┘',end='')

		# Drawing the heavy box bottom border
		# print(BD.BOT.L.h+ BD.HOR.h * (full_box_width - 2) + BD.BOT.R.h)


	# Example usage
	# sizes = [6, 5, 5]
	draw_rectangles(sizes)



# DEVS=['nvme0n1','nvme1n1','sda','sdb','sdc']
# for DEV in DEVS:
# 	print()
# 	draw_drive(DEV,term )

# print()
# for pair in sss:
# 	print(f'\x1b[{pair[0]}G┌',end='')
# 	print(f'\x1b[{pair[1]-1}G┐',end='')
# for pair in sss:
# 	print(pair)
def shell(cmd,**k):
	cmd=cmd.format(**k)
	return getoutput(cmd).split('\n')
import re
from re import MULTILINE,VERBOSE,DOTALL,compile,search


def sgdisk_parser(dev):
	parsed=Clict()
	'''example:
	Disk /dev/sdc: 3907029168 sectors, 1.8 TiB
	Model: ST2000DM008-2FR1 //we'll get this later with lsblk
	Disk identifier (GUID): 3D9017E0-7DC8-03AA-F805-640F729FEA00
	Partition table holds up to 128 entries
	Main partition table begins at sector 2 and ends at sector 33
	First usable sector is 34, last usable sector is 3907029134
	Partitions will be aligned on 8-sector boundaries
	Total free space is 2105453 sectors (1.0 GiB)
	'''
	cmd='sgdisk -p /dev/{DEV}'
	# Disk /dev/sdc: 3907029168 sectors, 1.8 TiB
	sgdisk=shell(cmd, DEV=dev)
	sectpart=print(shell("echo $(sgdisk -p /dev/{DEV}|tail -n +12  |awk '{AWK}')",DEV=dev,AWK='{print $2,$3 }')[0].split())
	lastsec=sgdisk[0]
	ptable,pspace=sgdisk[5:7]
	reend=r'Disk.*?: (?P<SIZE>\d+) sectors,.*'
	rept = r'Main partition table begins at sector (?P<STRT>\d+) and ends at sector (?P<STP>\d+)'
	reps = r'First usable sector is (?P<PSSTART>\d+), last usable sector is (?P<PSSTOP>\d+)'
	match = re.search(reend, lastsec)
	se=match.groupdict()
	match = re.search(rept, ptable)
	pt=match.groupdict()
	match = re.search(reps, pspace)
	ps=match.groupdict()
	gptsize=(gptstart:=int(pt['STP']))-(gptstop:=int(pt['STRT']))

	p=Clict()
	p.lastsector=int(se['SIZE'])
	p.section[0].type='MBR'
	p.section[0].size.sectors=1
	p.section[0].start.sectors=0
	p.section[0].stop.sectors=1
	p.section[1].type='GPT'
	p.section[1].size.sectors=gptsize
	p.section[1].start.sectors=gptstart
	p.section[1].stop.sectors=gptstop
	p.tables[0]=parsed.section[0]
	p.tables[1]=parsed.section[1]
	p.unalloc
	p.parts

	added=1
	scnt=2
	uacnt=0
	pcnt=0
	# input()
	while sectpart:
		# input()
		if added:
			nextp=sectpart.pop(0)
			added=0
		if p.section[scnt-1].stop.sectors+1 == nextp:
			s0=nextp
			s1=sectpart.pop(0)
			p.section[scnt].type='part'
			p.section[scnt].size.sectors=s1-s0
			p.section[scnt].start.sectors=s0
			p.section[scnt].stop.sectors=s1
			p.parts[scnt]=p.section[scnt]
			added=1
			scnt+=1
		else:
			s0=p.section[scnt-1].stop.sectors+1
			s1=nextp-1
			p.section[scnt].type='ua'
			p.section[scnt].size.sectors=s1-s0
			p.section[scnt].start.sectors=s0
			p.section[scnt].stop.sectors=s1
			p.unallocated[scnt]=p.section[scnt]
			added=0
			scnt+=1
			uacnt+=1
	# if p.lastsector > p.section[scnt-1].stop.sectors:
	# 	s0 = p.section[scnt].stop + 1
	# 	s1 = nextp - 1
	# 	p.section[scnt].type = 'ua'
	# 	p.section[scnt].size.sectors = s1 - s0
	# 	p.section[scnt].start.sectors = s0
	# 	p.section[scnt].stop.sectors = s1


	p.fromshell=sgdisk
	return p



def get_disks():
	disks=Clict()
	cmd = 'lsblk --noheadings  -dI 8,259 -o NAME,PATH'
	pttype='lsblk --noheadings -d -o PTTYPE {DEV}'
	disklist=[l.split() for l in getoutput(cmd).split('\n')]
	for disk in disklist:
		disks[disk[0]].name=disk[0]
		disks[disk[0]].path=disk[1]
		disks[disk[0]].parttable.type = getoutput(pttype.format(DEV=disk[1])).upper()
	return  disks

def sgdisk_boundaries(disk,ptstart,start,stop):
	bdlist=[0,ptstart,start]
	cmd_1="sgdisk -p /dev/{DEV} ".format(DEV=disk)
	cmd_2="tail -n  +12"
	cmd_3="awk '{print $2, $3}'"
	cmd=f'{cmd_1}|{cmd_2}|{cmd_3}'
	stdout=getoutput(cmd).split('\n')
	for l in stdout:
		for sec in l.split(' '):
			bdlist+=[int(sec)]
	sectionlist=[]
	for i,bound in enumerate(bdlist):
		nextbd=bdlist[i+1]
		if not nextbd == bound:
			sectionlist+=[(bound,bdlist[i+1])]
		if bound==bdlist[-2]:
			break
	return sectionlist


# def getSections(boundaries):
# 	sections = Clict()
# 	for i, section in enumerate(boundaries):
# 		sections[i].sectors.start = section[0]
# 		sections[i].sectors.stop = section[1]
# 		sections[i].sectors.size = section[1] - section[0]
# 	return sections
#

def get_parts(disk):
	parts=Clict()
	cmd='lsblk --list --noheadings  -I 8,259 -o PARTN,NAME,PATH {DEV}'
	partlist=[l.split() for l in getoutput(cmd.format(DEV=disk.path)).split('\n')[1:]]
	for part in partlist:
		parts[part[0]].path=part[2]
		parts[part[0]].name=part[1]
	disk.part=parts
	return disk

def get_partdata(d,p,part,bounds=[0,]):
	Part=part
	cmd='sgdisk -i {N} /dev/{DEV}'
	# print(cmd.format(N=p,DEV=d))
	sgdisk_info=getoutput(cmd.format(N=p,DEV=d)).split('\n')
	for line in sgdisk_info:
		key,value=line.split(':')
		Part.sgdisk[key.replace(' ','_')]=value
		part.sectors.start=Part.sgdisk.First_sector
		part.sectors.stop=Part.sgdisk.Last_sector
		# part.sectors.count=Part.sgdisk.Last_sector-Part.sgdisk.First_sector

	return part

def str2blk(line):
	BD.HOR.l = '─'
	BD.HOR.h = '━'
	BD.VER.l = '│'
	BD.VER.h = '┃'
	BD.TOP.L.l = '┌'
	BD.TOP.L.h = '┏'
	BD.TOP.R.l = '┐'
	BD.TOP.R.h = '┓'
	BD.BOT.L.l = '└'
	BD.BOT.L.h = '┗'
	BD.BOT.R.l = '┘'
	BD.BOT.R.h = '┛'
	BD.VERTICAL_SEPARATOR = '│'
	BD.HORIZONTAL_SEPARATOR = '┼'
	BD.MIDDLE_LEFT_LIGHT = '├'
	BD.MIDDLE_RIGHT_LIGHT = '┤'
	line=line.replace('F',BD.TOP.L.l)
	line=line.replace('T',BD.TOP.R.l)
	line=line.replace('L',BD.BOT.L.l)
	line=line.replace('J',BD.BOT.R.l)
	line=line.replace('-',BD.HOR.l)
	line=line.replace('|',BD.VER.l)
	return line


def get_partsectors(disk):
	return sgdisk_parser(disk)


def main():
	disks=get_disks()
	print('disks')
	for d in disks:
		if d!='sda':
			continue
		disks[d].hasMBR=True
		disks[d].hasGPT=True
		nscns=len(disks[d].sections)
		charspace=term.size[0]
		charspace=charspace-8
		sections=get_partsectors(d)
		sectleft=disks[d].size
		DT='\x1b[{DTL}G┏\x1b[{DTR}G┓\x1b[{DTL}G\x1b[C'
		chrcnt=2
		mbr=sections[0]
		DT+='┯'
		sectleft-=1
		gpt=sections[1]
		sectleft-=32
		DT9='━┳'
		pspace=sectleft
		div=disks[d].sections[-1][-1]
		# print(nscns,term.size[0],space,div)
		# print(disks['sda'].sections)
		def sc2chr(dsect,dchar):
			calc=lambda sect : (ttres:=int(tres:=(sect/dsect)*dchar))
			return calc
		chwidh=sc2chr(pspace,charspace)
		ST=''
		SB=''
		rt=0
		rtt=1
		tsss=''
		bsss=''
		for s,sect in enumerate(sections):
			sectsize=sect[1]['s']
			rtt += (crw:=chwidh(sectsize))
			print(sectsize*512/1024/1024/1024,crw,rt,charspace)
			tss=['─' for i in range(crw)]         #\x1b[{2+rtt-crw}G┌'+'┐'
			bss=['─' for i in range(crw)]         #\x1b[{2+rtt-crw}G┌'+'┐'
			if len(tss) < 2:
				tsss+=f'\x1b[{(rtt-crw)-1}G┐┌'
				bsss+=f'\x1b[{(rtt-crw)-1}G┘└'
			else:
				tss[0]=f'\x1b[{(rtt-crw)}G┌'
				tss[-1]='┐'
				bss[0]=f'\x1b[{(rtt-crw)}G└'
				bss[-1]='┘'
			ST+=''.join(tss)
			ST+=''.join(tsss)

			SB+='└'+''.join(bss)
			SB+=''.join(bsss)
			# SB+=f'\x1b[{2+rtt-crw}G└'+((-2+crw)*'-')+'┘'
			disks[d].sections[s][1]['c']=crw
		print(DT.format(space='━'*(charspace+8)))
		print(ST)
		print(SB)

			# if diffsca < 3:
			# 	inc=int(3-diffsca)
			# 	diffsca = 3
			# 	space-=inc
			# start=carry
			# end=(start+diffsca)-1
			# carry=end+1
			#
			#
			# scaled+=[[start,sect[1],end]]
		# print(disks['sda'].sections)
		# # print(scaled)
		# Tstr='┃'
		# Bstr='┃'
		# Mstr='┃'
		# DTSTR='\x1b[48;2;64;64;64m┏'+'━'*(scaled[-1][-1])+'┓'
		# DBSTR='┗'+'━'*(scaled[-1][-1])+'┛\x1b[m'
		# for item in scaled:
		# 	if item[1] != 'ua':
		# 		DASH='-'*((item[2]-item[0])-2)
		# 		Tstr+=f'\x1b[{item[0]+3}GF-{DASH}\x1b[{item[2]+3}GT'
		# 		Mstr+=f'\x1b[{item[0]+3}G|\x1b[{item[2]+3}G|'
		# 		Bstr+=f'\x1b[{item[0]+3}GL-{DASH}\x1b[{item[2]+3}GJ'
		#
		# 	else:
		# 		Tstr+=f'\x1b[{item[0]+1}G\x1b[{item[2]+2}G'
		# 		Mstr+=f'\x1b[{item[0]+1}G\x1b[{item[2]+2}G'
		# 		Bstr+=f'\x1b[{item[0]+1}G\x1b[{item[2]+2}G'
		# Tstr+='┃'
		# Bstr+='┃'
		# Mstr+='┃'
		# asciidisk=[DTSTR,Tstr,Mstr,Bstr,DBSTR]
		# blkdisk=[str2blk(l) for l in asciidisk]
		# print('\n'.join(blkdisk))

main()

# ab0db9
# ej1kl8
# im2en7
# op3rv6
# uw4z5.


'''
abfg0hjlm9
zexnxhpw81
i     72
o     63
u     54
			#
			# print(f'[{disks[d].sections[sect].sectors.start}---{disks[d].sections[sect].sectors.size}---{disks[d].sections[sect].sectors.stop}]',end='')
		# print()
		# for key in disks[d]:
		# 	if key == 'part':
		# 		continue
		# 	print(key,f'\x1b[20G:\x1b[60G{disks[d][key]}')
		#
		# for p in disks[d].part:
		# 	print('-',disks[d].part[p].name)
		# 	for key in disks[d].part[p].sgdisk:
		# 		print('   -',key,':',disks[d].part[p].sgdisk[key])
# print(getoutput('sgdisk -i 1 /dev/nvme0n1'))
# '''
# 	Disk /dev/sdc: 3907029168 sectors, 1.8 TiB
# 	Model: ST2000DM008-2FR1
# 	Sector size (logical/physical): 512/4096 bytes
# 	Disk identifier (GUID): 3D9017E0-7DC8-03AA-F805-640F729FEA00
# 	Partition table holds up to 128 entries
# 	Main partition table begins at sector 2 and ends at sector 33
# 	First usable sector is 34, last usable sector is 3907029134
# 	Partitions will be aligned on 8-sector boundaries
# 	Total free space is 2105453 sectors (1.0 GiB)
# 	---------------------------------------------
# 	Disk /dev/sdc: {SECTORS_TOTAL} sectors, {BYTES_SI_TOTAL} {BYTES_SI_TOTAL_SIPFX}iB
# 	Model: ST2000DM008-2FR1
# 	Sector size (logical/physical): {LOGSEC_BYTES}/{PHYSEC_BYTES} bytes
# 	Disk identifier (GUID): {DISK_UUID}
# 	Partition table holds up to {TABLE_MAX_ENTRIES} entries
# 	Main partition table begins at sector {MAIN_PARTTABLE_SECTOR_START} and ends at sector {MAIN_PARTTABLE_SECTOR_STOP}
# 	First usable sector is {PARTSPACE_SECTOR_START}, last usable sector is {PARTSPACE_SECTOR_STOP}
# 	Partitions will be aligned on {SECTOR_BD_SIZE}-sector boundaries
# 	Total free space is {SECTORS_FREE_TOTAL} sectors ({BYTESSI_FREE_TOTAL} {BYTESSI_FREE_TOTAL}iB)
# '''
# #create a python function that parses the folowing information out of the example text above:
# 	parsed={
# 		'SECTORS_TOTAL' : 3907029168,
# 		'BYTES_SI_TOTAL' : 1.8,
# 		'BYTES_SI_TOTAL_SIPFX':'T'
# 	...
# 	}
# 	return parsed
#
# 	}
# disk:
# 	sectors.total
# 	sectors.unallocated
# 	sectors.alignment
# 	pt.mbr
# 	pt.gpt
# 	pt.gpt.start
# 	pt.gpt.stop
#
#
# # section:
# # 	sector.start
# # 	sector.stop
# 	sector.total
# 	sector.free
