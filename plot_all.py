#################################################################################
# Created by Han-Mo Ou 070722 modified 093022 
# Python Plots for IMC Benchmarking
# Based on Matlab Code by Saion Roy & Naresh Shanbhag
# University of Illinois at Urbana-Champaign
#################################################################################
import os
import csv 
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import markers

##################################################################
######################## User Settings ###########################
##################################################################
# Set CSV Path
CSV_FILE = 'Benchmarking_Data.csv'

# Set Output Directory
OUTPUT_DIR = 'figures'

# Set Output Formats
SAVE_PDF = True
SAVE_SVG = True

# Plot Rectangle for IMC Processors 
MARK_IMC_PROCESSOR = [1, 1, 1, 0, 1, 1, 1]

##################################################################
##################################################################

# Create Output Directory
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

if SAVE_PDF:
    if not os.path.exists(OUTPUT_DIR + '/pdf'):
        os.mkdir(OUTPUT_DIR + '/pdf')

if SAVE_SVG:
    if not os.path.exists(OUTPUT_DIR + '/svg'):
        os.mkdir(OUTPUT_DIR + '/svg')


# List of Technology and Architectures to Loop
TECH_LIST = [5,7,12,16,22,28,45,55,65,180]
ARCH_LIST = ['SRAM', 'eNVM', 'eDRAM', 'Digital']
ARCH_LABEL_LIST = ['SRAM-IMC', 'eNVM-IMC', 'eDRAM-IMC', 'Digital']


# Pyplot Variables
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['legend.loc'] = 'lower right'
plt.rcParams['font.family'] = 'calibri'

FIG_SIZE = (9.8, 7.8)
COLORS = {'r': 'r', 'g': 'lawngreen', 'b':'b', 'c': 'cyan', 'k': 'k'}
GRID_ALPHA = 0.4


# Pyplot Red Box 
red_box_style = markers.MarkerStyle([(-1,-1), (-1,1), (1,1), (1,-1)], 'none')

# Empty Class to Store Data
class Data: 
    pass

# Collect all data from CSV file
def fetch_data():
    with open(CSV_FILE, encoding='utf-8') as file:
        # Load CSV File
        reader = list(csv.DictReader(file)) 

        # Replacing Empty Strings in CSV
        for row in reader:
            for key in row:
                row[key] = row[key].rstrip(' ')
                if row[key] == '':
                    row[key] = float('NAN')
                    
        data = Data()

        # Converting CSV Data to Array
        data.TOPS_mm2     = np.array([row['TOPS/mm2'] for row in reader], dtype = np.float32)
        data.TOPS_W       = np.array([row['TOPS/W'] for row in reader], dtype = np.float32)
        data.B_pre_ADC    = np.array([row['B_pre-ADC'] for row in reader], dtype = np.float32)
        data.Tech         = np.array([row['Tech (nm)'] for row in reader], dtype = np.int32)
        data.Year         = np.array([row['Year'] for row in reader], dtype = np.float32)
        data.core_size    = np.array([row['Core Size(Kb)'] for row in reader], dtype = np.float32)
        data.N_row        = np.array([row['N_row'] for row in reader], dtype = np.float32)
        data.N_col        = np.array([row['N_col'] for row in reader], dtype = np.float32)
        data.Vdd          = np.array([row['Supply V(V)'] for row in reader])
        data.B_X          = np.array([row['B_x'] for row in reader], dtype = np.float32)
        data.B_W          = np.array([row['B_w'] for row in reader], dtype = np.float32)
        data.B_ADC        = np.array([row['B_ADC'] for row in reader], dtype = np.float32)
        data.R_C          = np.array([row['R_C'] for row in reader], dtype = np.float32)
        data.R            = np.array([row['R'] for row in reader], dtype = np.float32)
        data.C_C          = np.array([row['C_C'] for row in reader], dtype = np.float32)
        data.C            = np.array([row['C'] for row in reader], dtype = np.float32)
        data.N_ADC        = np.array([row['N_ADC'] for row in reader], dtype = np.float32)
        data.N            = np.array([row['N'] for row in reader], dtype = np.float32)
        data.N_1b         = np.array([row['N_1b'] for row in reader], dtype = np.float32)
        data.B_core       = np.array([row['B_core'] for row in reader], dtype = np.float32)
        data.alpha        = np.array([row['alpha'] for row in reader], dtype = np.float32)
        data.B_col        = data.B_X * data.R_C * data.C_C
        data.T_core_ns    = np.array([row['T_core(ns)'] for row in reader], dtype = np.float32)
        data.E_OP1_fJ     = np.array([row['E_OP1 (fJ)'] for row in reader], dtype = np.float32)
        data.N_core       = np.array([row['N_core'] for row in reader], dtype = np.float32)
        data.E_col_fJ     = np.array([row['E_col (fJ)'] for row in reader], dtype = np.float32)
        data.E_core_pJ    = np.array([row['E_core (pJ)'] for row in reader], dtype = np.float32)
        data.E_mvm_pJ     = np.array([row['E_mvm (pJ)'] for row in reader], dtype = np.float32)
        data.Cell_Type    = [row['Cell Type'] for row in reader]
        data.Compute_Mod  = [row['Compute Model'] for row in reader]
        data.Arch         = [row['Architecture'] for row in reader]
        data.TOPS_a       = np.array([row['TOPS_a '] for row in reader], dtype = np.float32)
        data.TOPS         = np.array([row['TOPS'] for row in reader], dtype = np.float32)
        data.IMC_Proc      = np.array([row['IMC_Processor'] == 'Y' for row in reader], dtype = np.int32)
        
    return data


# SRAM: TOPS/W vs. TOPS/mm^2 (with TSMC paper)
def plot_1(data): 
    
    fig, ax = plt.subplots(figsize = FIG_SIZE)
    
    colors = 'rrggbbcckk'
    marker = 'ososososos'
    marker_size = 100 
    
    for j, tech in enumerate(TECH_LIST):
        SRAM_tech = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == 'SRAM' and data.Tech[i] == tech])
        ax.scatter(data.TOPS_mm2[SRAM_tech], data.TOPS_W[SRAM_tech], marker_size, COLORS[colors[j]], marker[j], label = '%dnm'%tech)
        if MARK_IMC_PROCESSOR[0]:
            SRAM_tech = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == 'SRAM' and data.Tech[i] == tech and data.IMC_Proc[i] == 1])
            if len(SRAM_tech):
                ax.plot(data.TOPS_mm2[SRAM_tech], data.TOPS_W[SRAM_tech], 'ks',markerfacecolor='none', ms=18, markeredgecolor='red', markeredgewidth = 1.5 )
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(which = 'both', alpha = GRID_ALPHA, linestyle = 'dotted')
    
    ax.legend(fontsize = 12)
    ax.set_title('Energy-efficiency vs. Compute Density', fontsize = 15, fontweight = 'bold')
    ax.set_xlabel('1b-TOPS/mm$^2$', fontsize = 15)
    ax.set_ylabel('1b-TOPS/W', fontsize = 15)

    if SAVE_SVG:
        fig.savefig(OUTPUT_DIR + '/svg/1_1b-TOPSpW_vs_1bTOPSpmm2_SRAM.svg', bbox_inches = 'tight')
    if SAVE_PDF:
        fig.savefig(OUTPUT_DIR + '/pdf/1_1b-TOPSpW_vs_1bTOPSpmm2_SRAM.pdf', bbox_inches = 'tight')


# SRAM: TOPS/W vs. TOPS
def plot_2(data):
    fig, ax = plt.subplots(figsize = FIG_SIZE)
    
    colors = 'rrggbbcckk'
    marker = 'ososososos'
    marker_size = 100 
    
    for j, tech in enumerate(TECH_LIST):
        SRAM_tech = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == 'SRAM' and data.Tech[i] == tech])
        ax.scatter(data.TOPS[SRAM_tech], data.TOPS_W[SRAM_tech], marker_size, COLORS[colors[j]], marker[j], label = '%dnm'%tech)
        # for idx in range(len(SRAM_tech)):
            # print(SRAM_tech, data.TOPS[SRAM_tech][idx], data.TOPS_W[SRAM_tech][idx], data.Cell_Type[SRAM_tech[idx]])
            # print()
            # ax.annotate(data.Cell_Type[SRAM_tech[idx]], (data.TOPS[SRAM_tech][idx], data.TOPS_W[SRAM_tech][idx]), xytext=(0, 5), textcoords='offset points')        
        if MARK_IMC_PROCESSOR[1]:
            SRAM_tech = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == 'SRAM' and data.Tech[i] == tech and data.IMC_Proc[i] == 1])
            if len(SRAM_tech):
                ax.plot(data.TOPS[SRAM_tech], data.TOPS_W[SRAM_tech], 'ks',markerfacecolor='none', ms=18, markeredgecolor='red', markeredgewidth = 1.5 )
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(which = 'both', alpha = GRID_ALPHA, linestyle = 'dotted')
    
    ax.legend(fontsize = 12)
    ax.set_title('Energy Efficiency vs. Throughput', fontsize = 15, fontweight = 'bold')
    ax.set_xlabel('1b-TOPS/mm$^2$', fontsize = 15)
    ax.set_xlabel('1b-TOPS', fontsize = 15)
    ax.set_ylabel('1b-TOPS/W', fontsize = 15)

    if SAVE_SVG:
        fig.savefig(OUTPUT_DIR + '/svg/2_1b-TOPSpW_vs_1b-TOPS_SRAM.svg')
    if SAVE_PDF:
        fig.savefig(OUTPUT_DIR + '/pdf/2_1b-TOPSpW_vs_1b-TOPS_SRAM.pdf')


# SRAM: TOPS/W vs. B_I_col
def plot_3(data):
    fig, ax = plt.subplots(figsize = FIG_SIZE)
    
    colors = 'rrggbbcckk'
    marker = 'ososososos'
    marker_size = 100 
    
    for j, tech in enumerate(TECH_LIST):
        SRAM_tech = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == 'SRAM' and data.Tech[i] == tech])
        ax.scatter(data.B_pre_ADC[SRAM_tech], data.TOPS_W[SRAM_tech], marker_size, COLORS[colors[j]], marker[j], label = '%dnm'%tech)
        if MARK_IMC_PROCESSOR[2]:
            SRAM_tech = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == 'SRAM' and data.Tech[i] == tech and data.IMC_Proc[i] == 1])
            if len(SRAM_tech):
                ax.plot(data.B_pre_ADC[SRAM_tech], data.TOPS_W[SRAM_tech], 'ks',markerfacecolor='none', ms=18, markeredgecolor='red', markeredgewidth = 1.5 )
    
    ax.set_yscale('log')
    ax.grid(which = 'both', alpha = GRID_ALPHA, linestyle = 'dotted')
    
    ax.legend(fontsize = 12)
    ax.set_title('Energy-efficiency vs. Pre-ADC Information Content', fontsize = 15, fontweight = 'bold')
    ax.set_xlabel('1b-TOPS/mm$^2$', fontsize = 15)
    ax.set_xlabel('$B_{I(col)}$ (bits)', fontsize = 15)
    ax.set_ylabel('1b-TOPS/W', fontsize = 15)

    if SAVE_SVG:
        fig.savefig(OUTPUT_DIR + '/svg/3_1b-TOPSpW_vs_BIcol_SRAM.svg')
    if SAVE_PDF:
        fig.savefig(OUTPUT_DIR + '/pdf/3_1b-TOPSpW_vs_BIcol_SRAM.pdf')


# SRAM: B_ADC vs. B_pre_ADC
def plot_4(data):
    fig, ax = plt.subplots(figsize = FIG_SIZE)
    
    colors = 'rrggbbcckk'
    marker = 'ososososos'
    marker_size = 100 
    
    for j, tech in enumerate(TECH_LIST):
        SRAM_tech = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == 'SRAM' and data.Tech[i] == tech])
        ax.scatter(data.B_pre_ADC[SRAM_tech], data.B_ADC[SRAM_tech], marker_size, COLORS[colors[j]], marker[j], label = '%dnm'%tech)
        if MARK_IMC_PROCESSOR[3]:
            SRAM_tech = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == 'SRAM' and data.Tech[i] == tech and data.IMC_Proc[i] == 1])
            if len(SRAM_tech):
                ax.plot(data.B_pre_ADC[SRAM_tech], data.B_ADC[SRAM_tech], 'ks',markerfacecolor='none', ms=18, markeredgecolor='red', markeredgewidth = 1.5 )
    ax.plot(np.arange(12), np.arange(12), 'k--', label = '$B_{ADC} = B_{I(col)}$')
    
    ax.grid(which = 'both', alpha = GRID_ALPHA, linestyle = 'dotted')
    
    ax.legend(fontsize = 12)
    ax.set_title('ADC Precision vs. Pre-ADC Information Content', fontsize = 15, fontweight = 'bold')
    ax.set_xlabel('1b-TOPS/mm$^2$', fontsize = 15)
    ax.set_xlabel('$B_{I(col)}$ (bits)', fontsize = 15)
    ax.set_ylabel('$B_{ADC}$ (bits)', fontsize = 15)

    if SAVE_SVG:
        fig.savefig(OUTPUT_DIR + '/svg/4_BADC_vs_BIcol_SRAM.svg')
    if SAVE_PDF:
        fig.savefig(OUTPUT_DIR + '/pdf/4_BADC_vs_BIcol_SRAM.pdf')


# Grouping by Architecture: SRAM/eNVM/Dig: TOPS/W vs. TOPS (with TSMC paper)
def plot_5(data):
    fig, ax = plt.subplots(figsize = FIG_SIZE)
    
    colors = 'gbkr'
    marker = 'odos'
    marker_size = 100 
    
    for j, arch in enumerate(ARCH_LIST):
        archs = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i]  == arch])
        ax.scatter(data.TOPS[archs], data.TOPS_W[archs], marker_size, COLORS[colors[j]], marker[j], label = ARCH_LABEL_LIST[j])
        if MARK_IMC_PROCESSOR[4]:
            archs = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i]  == arch and data.IMC_Proc[i] == 1])
            if len(archs):
                ax.plot(data.TOPS[archs], data.TOPS_W[archs], 'ks',markerfacecolor='none', ms=18, markeredgecolor='red', markeredgewidth = 1.5 )
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(which = 'both', alpha = GRID_ALPHA, linestyle = 'dotted')
    
    ax.legend(fontsize = 12)
    ax.set_title('Energy-efficiency vs. Throughput for SRAM, eNVM, eDRAM, Digital', fontsize = 15, fontweight = 'bold')
    ax.set_xlabel('1b-TOPS/mm$^2$', fontsize = 15)
    ax.set_xlabel('1b-TOPS', fontsize = 15)
    ax.set_ylabel('1b-TOPS/W', fontsize = 15)

    if SAVE_SVG:
        fig.savefig(OUTPUT_DIR + '/svg/5_1b-TOPS_vs_1b-TOPSpW_all.svg')
    if SAVE_PDF:
        fig.savefig(OUTPUT_DIR + '/pdf/5_1b-TOPS_vs_1b-TOPSpW_all.pdf')

# Grouping by Architecture: SRAM/eNVM/Dig: TOPS/W vs. TOPS (with TSMC paper)
def plot_6(data):
    fig, ax = plt.subplots(figsize = FIG_SIZE)
    
    colors = 'gbkr'
    marker = 'odos'
    marker_size = 100 
    
    for j, arch in enumerate(ARCH_LIST):
        archs = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == arch])
        ax.scatter(data.TOPS_mm2[archs], data.TOPS_W[archs], marker_size, COLORS[colors[j]], marker[j], label = ARCH_LABEL_LIST[j])
        if MARK_IMC_PROCESSOR[5]:
            archs = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i]  == arch and data.IMC_Proc[i] == 1])
            if len(archs):
                ax.plot(data.TOPS_mm2[archs], data.TOPS_W[archs], 'ks',markerfacecolor='none', ms=18, markeredgecolor='red', markeredgewidth = 1.5 )
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(which = 'both', alpha = GRID_ALPHA, linestyle = 'dotted')
    
    ax.legend(fontsize = 12)
    ax.set_title('Energy-efficiency vs. Compute Density for SRAM, eNVM, eDRAM, Digital', fontsize = 15, fontweight = 'bold')
    ax.set_xlabel('1b-TOPS/mm$^2$', fontsize = 15)
    ax.set_xlabel('1b-TOPS/mm$^2$', fontsize = 15)
    ax.set_ylabel('1b-TOPS/W', fontsize = 15)

    if SAVE_SVG:
        fig.savefig(OUTPUT_DIR + '/svg/6_1b-TOPSpmm2_vs_1b-TOPSpW_all.svg', bbox_inches = 'tight')
    if SAVE_PDF:
        fig.savefig(OUTPUT_DIR + '/pdf/6_1b-TOPSpmm2_vs_1b-TOPSpW_all.pdf', bbox_inches = 'tight')

# Grouping by Architecture: SRAM/eNVM/Dig: TOPS vs. W
def plot_7(data):
    fig, ax = plt.subplots(figsize = FIG_SIZE)
    
    colors = 'gbkr'
    marker = 'odos'
    marker_size = 100 
    
    for j, arch in enumerate(ARCH_LIST):
        archs = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i] == arch])
        ax.scatter(data.TOPS[archs] / data.TOPS_W[archs], data.TOPS[archs], marker_size, COLORS[colors[j]], marker[j], label = ARCH_LABEL_LIST[j])
        if MARK_IMC_PROCESSOR[6]:
            archs = np.array( [i for i in range(len(data.Arch)) if  data.Arch[i]  == arch and data.IMC_Proc[i] == 1])
            if len(archs):
                ax.plot(data.TOPS[archs] / data.TOPS_W[archs], data.TOPS[archs], 'ks',markerfacecolor='none', ms=18, markeredgecolor='red', markeredgewidth = 1.5 )
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(which = 'both', alpha = GRID_ALPHA, linestyle = 'dotted')
    
    ax.legend(fontsize = 12)
    ax.set_title('Throughput vs. Power for SRAM, eNVM, eDRAM, and Digital', fontsize = 15, fontweight = 'bold')
    ax.set_xlabel('1b-TOPS/mm$^2$', fontsize = 15)
    ax.set_xlabel('Power (W)', fontsize = 15)
    ax.set_ylabel('1b-TOPS', fontsize = 15)

    if SAVE_SVG:
        fig.savefig(OUTPUT_DIR + '/svg/7_1b-TOPS_vs_W_all.svg')
    if SAVE_PDF:
        fig.savefig(OUTPUT_DIR + '/pdf/7_1b-TOPS_vs_W_all.pdf')
    

# Plot all figures
def main():
    data = fetch_data()
    plot_1(data)
    plot_2(data)
    plot_3(data)
    plot_4(data)
    plot_5(data)
    plot_6(data)
    plot_7(data)


# Main
if __name__ == '__main__':
    main()
