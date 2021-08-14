#!/usr/bin/env python
"""
The backend helper scripts for comparing different
samples/cuts/variables from histograms.
"""

########################################
# Imports and setup ROOT with style
########################################

import sys
import glob
import os
import ROOT
from array import array

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
   import TTH.Plotting.Helpers.OutputDirectoryHelper as OutputDirectoryHelper
   from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
# Without CMSSW
else:
   import TTH.Plotting.python.Helpers.OutputDirectoryHelper as OutputDirectoryHelper
   from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle

# initializer: simple creation of bag-of-object classes
from Initializer import initializer

#myStyle.SetPadLeftMargin(0.12)
#myStyle.SetPadTopMargin(0.06)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# class combinedPlot:
########################################

class combinedPlot:
    """Helper Class to Configure Plots"""
   
    # Static member variable. Add all objects to this list
    # to be able to draw them at once.
    li_combined_plots = []

    @initializer
    def __init__(self, 
                name,
                li_plots,
                nbins_x,
                min_x,
                max_x,
                max_y           = None,
                label_x         = "",
                label_y         = "",                
                axis_unit       = "",
                log_y           = False,
                normalize       = False,
                scale           = False,
                draw_legend     = True,
                legend_origin_x = 0.52,
                legend_origin_y = 0.7, 
                legend_size_x   = 0.2,
                legend_size_y   = -1,
                legend_text_size= 0.05,
                get_ratio = False,
                ratiomin = 0.75,
                ratiomax = 1.25
                ):
        """ Constructor. Arguments:
        name            : (string) name for output file
        li_plots        : (list of plot objects) plots to combine
        nbins_x         : (int) number of bins to use for the x-axis
        min_x           : (float) minimal x-value
        max_x           : (float) maximal x-value
        max_y           : (float) maximal y-value
        label_x         : (string) label for the x-axis (unit is added)
        label_y         : (string) label for the y-axis ( / binwidth and unit are added) 
        axis_unit       : (string) unit for the x-axis (added to x- and y-labels)
        log_y           : (bool) logarithmic y-axis
        normalize       : (bool) area-normalize the graphs
        draw_legend     : (bool) draw the legend
        legend_origin_x : (float) position of the left? edge of the legend
        legend_origin_y : (float) position of the upper? edge of the legend
        legend_size_x   : (float) horizontal extension of the legen
        legend_size_y   : (float) vertical extension of the legend        
        legend_text_size: (float) text size of the legend    
        get_ratio       : (bool) get ratio between distributions   
        ratiomin        : (float) min of ratio plot
        ratiomax        : (float) max of ratio plot
        """ 

        # Add to the static member for keeping track of all objects
        self.__class__.li_combined_plots.append( self )
# End of class combinedPlot     


class combinedPlot2D:
    """Helper Class to Configure Plots"""
   
    # Static member variable. Add all objects to this list
    # to be able to draw them at once.
    li_combined_plots2D = []

    @initializer
    def __init__(self, 
                name,
                li_plots2D,
                nbins_x,
                min_x,
                max_x,
                nbins_y,
                min_y,
                max_y,
                label_x         = "",
                label_y         = "",                
                axis_unit       = "",
                log_y           = False,
                option = None,
                normalize       = False,
                ):
        """ Constructor. Arguments:
        name            : (string) name for output file
        li_plots2D        : (list of plot objects) plots to combine
        nbins_x         : (int) number of bins to use for the x-axis
        min_x           : (float) minimal x-value
        max_x           : (float) maximal x-value
        nbins_y         : (int) number of bins to use for the y-axis
        min_y           : (float) minimal y-value
        max_y           : (float) maximal y-value
        label_x         : (string) label for the x-axis (unit is added)
        label_y         : (string) label for the y-axis ( / binwidth and unit are added) 
        axis_unit       : (string) unit for the x-axis (added to x- and y-labels)
        log_y           : (bool) logarithmic y-axis
        option          : (bool) Write bin Content for TH2D histograms
        normalize       : (bool) If maximum should be set to one
        """

        # Add to the static member for keeping track of all objects
        self.__class__.li_combined_plots2D.append( self )
# End of class combinedPlot2


class plot:
    @initializer
    def __init__(self, 
                name,
                var,
                cut,
                from_file,
                scale = -1,
                color = "default",
                linestyle = 1,
                fillstyle = "default",
                scale_cut="",
                fit = None,
                error = False
             ):
        """ Constructor. Arguments:
        name        : (string) name to use for the legend
        var         : (string) variable to plot
        cut         : (string) cut to apply
        from_file   : (string, key in dic_files): which distribution to draw
        scale       : (float) by how much to scale the histogram, default: not scaled
        linestyle   : (int) which linestyle to use
        scale_cut   : (string) scale the histogram by 1/#entries passing the cut
        fit         : (TF1) function to fit. Warning: fitting only works if
                              exactly one plot is added to combinedPlots
        error       : (bool) flag if errors should be drawn
        """
        pass
# End of class plot 


########################################
# Formatting/nice text defintions
########################################

# List of nice plotting colors
li_colors = [ROOT.kBlack, 
             ROOT.kRed, 
             ROOT.kBlue, 
             28, 
             #ROOT.kOrange, 
             ROOT.kGray, 
             ROOT.kGreen, 
             ROOT.kMagenta, 
             ROOT.kCyan,
             ROOT.kOrange+3
          ]*10

# List of nice line style
li_line_styles = [1]*len(li_colors) + [4]*len(li_colors) + [2]*len(li_colors)



c = ROOT.TCanvas("","",800,800)
c.SetLeftMargin(0.16)
c.SetGrid() 
W = 600
H = 600
H_ref = 600
W_ref = 600
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

c.SetLeftMargin(0.16)
c.SetRightMargin(R/W)
c.SetTopMargin(T/H)
c.SetBottomMargin(B/H)
#c.SetRightMargin(0.16)



########################################
# Create histograms
########################################

def createHistograms(dic_files):

    # Dictionary to store the histograms in
    # key: combinedPlot.name _ plot.name
    dic_histos = {}
    dic_histos2D = {}

    # Count the draw commands. This way wec can
    # assign unique names to the histograms:
    # htmpX
    i_draw = 0

    for cp in combinedPlot.li_combined_plots:

        for p in cp.li_plots:

            # Retrieve the histogram
            if len(dic_files[p.from_file])== 3:
                f =  ROOT.TFile(dic_files[p.from_file][0]) 
                f.cd(dic_files[p.from_file][1])
                t = f.Get("Events")
                t.Draw("{}>>hint".format(p.var))
                h = ROOT.gDirectory.Get("hint")
            elif len(dic_files[p.from_file])== 2:
                f =  ROOT.TFile(dic_files[p.from_file][0]) 
                t = f.Get(dic_files[p.from_file][1])
                t.Draw("{}>>hint".format(p.var))
                h = ROOT.gDirectory.Get("hint")
            else :   
                print dic_files[p.from_file]
                f =  ROOT.TFile(dic_files[p.from_file]) 
                h = getattr(f, p.var)
            #h = f.p.var
            #h.Draw()
            h.SetDirectory(0)

            if p.scale>0:
                h.Scale(p.scale)

            # Optional: scale the histogram by 1/#entries passing a cut
            if not(p.scale_cut==""):
                htmp_cut_name= "htmp_cut"+str(i_draw)
                li_cut_string = [p.var, 
                                ">>", htmp_cut_name]

                cut_string = "".join(li_cut_string)
           
                input_tree.Draw( cut_string, p.scale_cut , "goff")

                # Retrieve the histogram
                h_cut = ROOT.gDirectory.Get(htmp_cut_name).Clone()
                h_cut.SetDirectory(0)
           
                n_entries_cut=h_cut.Integral()
                if(n_entries_cut==0):
                    print "No entry passing the cut"
                else:
                    h.Scale(1./n_entries_cut)

            i_draw += 1
        
            # Save the histogram in the dictionary
            dic_histos[cp.name + "_" + p.name] = h

        # end of variable loop
    # end of input_file loop


    for cp in combinedPlot2D.li_combined_plots2D:

        for p in cp.li_plots2D:

            # Retrieve the histogram
            f =  ROOT.TFile(dic_files[p.from_file]) 
            h = getattr(f, p.var)
            #h = f.p.var
            #h.Draw()
            h.SetDirectory(0)
    
            i_draw += 1
            
            # Save the histogram in the dictionary
            dic_histos2D[cp.name + "_" + p.name] = h

        # end of variable loop
    # end of input_file loop

    return dic_histos,dic_histos2D

# end of createHistograms


########################################
# Draw Histograms
########################################

def drawHistograms(dic_histos, dic_histos2D, output_dir):

    ROOT.TGaxis.SetMaxDigits(4)

    # Define and create output directory
    OutputDirectoryHelper.CreateOutputDirs( output_dir )

    # Loop over combinedPlots
    for cp in combinedPlot.li_combined_plots:

        if cp.legend_size_y==-1:
           cp.legend_size_y = cp.legend_text_size * 1.25 * len(cp.li_plots)

        # Init the Legend
        leg = ROOT.TLegend( cp.legend_origin_x,
                            cp.legend_origin_y,
                            cp.legend_origin_x + cp.legend_size_x,
                            cp.legend_origin_y + cp.legend_size_y )
        leg.SetFillColor(0)
        leg.SetLineColor(0)
        leg.SetTextSize(cp.legend_text_size)
        leg.SetShadowColor(0)

                  
        # Optional: normalize area to one
        if cp.normalize:
            for p in cp.li_plots:
                h = dic_histos[cp.name + "_" + p.name]
                if h.Integral():
                    h.Scale( 1/h.Integral())

        if cp.scale:
            for p in cp.li_plots:
                h = dic_histos[cp.name + "_" + p.name]
                scale = h.GetXaxis().GetBinWidth(1)/(h.Integral())
                print "scaling..."
                norm = 1;
                h.Scale(norm/h.Integral(), "width")

        # Optional: rebin histogram
        if cp.nbins_x:
            for p in cp.li_plots:
                h = dic_histos[cp.name + "_" + p.name]
                factor = float(h.GetNbinsX()/cp.nbins_x)
                h.Rebin(h.GetNbinsX()/cp.nbins_x)
                if factor>1:
                    h.Scale(1/factor)
                  
        # If not set, determine the y-range
        if cp.max_y == None:

            # Find the maximum y-value of the histgorams
            found_max = max([dic_histos[cp.name + "_" + p.name].GetMaximum() for p in cp.li_plots])

            # Set the y-range accordingly
            # extend furhter for logarithmic y-axes
            if cp.log_y:
                cp.max_y = 2*found_max
            else:
                cp.max_y = 1.25*found_max
                # End of cp.max_y == None

        if cp.get_ratio:
            pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
            pad1.SetBottomMargin(0)        
            pad1.Draw()          
            pad1.cd()  
            r = {}

        usedcolors = []
        # Loop over plots
        for i_p, p in enumerate(cp.li_plots):

            # Get the histogram
            h = dic_histos[cp.name + "_" + p.name]
            
            if cp.get_ratio:
                r[i_p] = h.Clone()
                if cp.get_ratio and i_p>0:
                    r[i_p].Divide(r[0])
                    for k in range (1,r[i_p].GetNbinsX()+1):
                        if r[i_p].GetBinContent(k) == 0:
                            r[i_p].SetBinContent(k,1)

            # Get colors/ls
            if p.color is not "default":
                if "+" in p.color:
                    pc = p.color.split("+")
                    color = getattr(ROOT,pc[0])+int(pc[1])
                elif "-" in p.color:
                    pc = p.color.split("-")
                    color = getattr(ROOT,pc[0])-int(pc[1])
                else:   
                    color = getattr(ROOT,p.color)
            else:
                color = li_colors[i_p]
            usedcolors.append(color)
            ls = li_line_styles[i_p]

            print color

            # Colorize/set linestyle
            h.SetLineWidth( 3 )
            h.SetLineColor( color )
            h.SetLineStyle( ls ) 
            if p.linestyle != 1:
                h.SetLineStyle(p.linestyle)     
            #h.SetFillColor(0)
            if p.fillstyle is not "default":
                h.SetFillColor(color)
                h.SetFillColorAlpha(color, 0.55);
                h.SetFillStyle(p.fillstyle)
                h.SetLineWidth(0)

            # add to legend
            if p.fillstyle is not "default":
                leg.AddEntry( h, p.name,  "f")
            else:
                leg.AddEntry( h, p.name, "l")


            # Adjust y-range        
            if cp.log_y:
                h.SetAxisRange(0.1, cp.max_y,"y")
                h.GetYaxis().SetLimits(0.01,cp.max_y)
                c.SetLogy(True)
            else:
                h.SetAxisRange(0.0001, cp.max_y,"y")
                h.GetYaxis().SetLimits(0,cp.max_y)
                c.SetLogy(False)
                # end of y-range adjusting

            # reduce number of ticks on x-axis
            #c1.SetLeftMargin(0.13)
            h.GetXaxis().SetRangeUser(cp.min_x,cp.max_x)
            # Label the x-axis
            # proper adding of [units] to the x-axis label
            bin_width = h.GetBinWidth( 1 )
            if not cp.get_ratio:
                if cp.axis_unit:
                    h.GetXaxis().SetTitle( cp.label_x + " [" + cp.axis_unit + "]")
                else:
                    h.GetXaxis().SetTitle( cp.label_x )

            # Label the y-axis
            #h.GetYaxis().SetTitle( cp.label_y + " / "+str(bin_width) +" "+ cp.axis_unit)
            h.GetYaxis().SetTitle( cp.label_y)
            
            h.GetYaxis().SetTitleOffset(1.7)
            if h.GetMaximum()>1 and h.GetMaximum()<100:
                h.GetYaxis().SetTitleOffset(0.5)
            if cp.get_ratio:
                h.GetYaxis().SetTitleOffset(0.5)

            print p.name, h.GetEntries()


            # Optional fit            
            if p.fit is not None:
                h.Fit(p.fit, "R")               

            # Draw the histogram
            if i_p == 0:

                #h.GetYaxis().SetNdivisions(410)
                if p.error == True:
                    h.Draw("HIST E0")
                    h.SetMarkerSize(0)
                else:
                    h.Draw("HIST")

                #txt = ROOT.TText()
                #txt.SetTextFont(61)
                #txt.SetTextSize(0.05)
                #txt.DrawTextNDC(0.18, 0.88, "CMS")
#
                #txt.SetTextFont(52)
                #txt.SetTextSize(0.04)
                #txt.DrawTextNDC(0.18, 0.84, "Private work")
#
                #txt.SetTextFont(41)
                #txt.DrawTextNDC(0.85, 0.95, "13 TeV")

                # Draw the legend
                if cp.draw_legend:
                    leg.Draw()

            else:
                if p.error == True:
                    h.Draw("HIST E0 SAME")
                    h.SetMarkerSize(0)
                else:
                    h.Draw("HIST SAME")
        
        #Now draw the ratio

        if cp.get_ratio:
            c.cd()  
            pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
            pad2.SetTopMargin(0)
            pad2.SetBottomMargin(0.3)
            #pad2.SetLeftMargin(0.3)
            pad2.Draw()
            pad2.cd()  
    
            for n in range(1,len(r)):

                # Get the histogram
                h = r[n]
    
                # Get colors/ls
                color = usedcolors[n]
                ls = li_line_styles[n]
    
                # Colorize/set linestyle
                h.SetLineWidth( 3 )
                h.SetLineColor( color )
                h.SetLineStyle( ls )      
                #h.SetFillColor(0)
    
                # Adjust y-range        
                if cp.log_y:
                    h.SetAxisRange(cp.ratiomin,cp.ratiomax,"y")
                    h.GetYaxis().SetLimits(0.01,cp.max_y)
                    c.SetLogy(True)
                else:
                    h.SetAxisRange(cp.ratiomin,cp.ratiomax,"y")
                    h.GetYaxis().SetLimits(0,cp.max_y)
                    c.SetLogy(False)
                    # end of y-range adjusting
    
                # reduce number of ticks on x and y-axis
                h.GetXaxis().SetNdivisions(5,5,0)
                h.GetYaxis().SetNdivisions(5,5,0)
                
                #Set range x-axis
                h.GetXaxis().SetRangeUser(cp.min_x,cp.max_x)
    
                # Set proper label sizes on ratio plot
                h.GetXaxis().SetLabelSize(0.7/0.25*h.GetXaxis().GetTitleSize())
                h.GetYaxis().SetLabelSize(0.7/0.25*h.GetYaxis().GetTitleSize())
    
                # Label the x-axis
                # proper adding of [units] to the x-axis label
                bin_width = h.GetBinWidth( 1 )
    
    
                if cp.axis_unit:
                    h.GetXaxis().SetTitle( cp.label_x + " [" + cp.axis_unit + "]")
                else:
                    h.GetXaxis().SetTitle( cp.label_x )
    
                h.GetXaxis().SetTitleOffset(1.05)
                h.GetXaxis().SetTitleSize(0.7/0.25*h.GetXaxis().GetTitleSize())
    
                # Label the y-axis
                #h.GetYaxis().SetTitle( cp.label_y + " / "+str(bin_width) +" "+ cp.axis_unit)
                h.GetYaxis().SetTitle("Ratio")
                h.GetYaxis().SetTitleOffset(0.3)
                h.GetYaxis().SetTitleSize(0.7/0.25*h.GetYaxis().GetTitleSize())
                h.SetMarkerSize(0)
    
                # Optional fit            
                if p.fit is not None:
                    h.Fit(p.fit, "R")               
    
                # Draw the histogram
                if n == 0:
                    h.GetYaxis().SetNdivisions(410)

                    h.Draw("SAME")
                    li = ROOT.TLine(0,1,0,1)
                    li.Draw("")
    
                else:
                    h.Draw("SAME")
                    li = ROOT.TLine(0,1,0,1)
                    li.Draw("")
    
         
        
        # Save the results to a file (in different formats)
        OutputDirectoryHelper.ManyPrint(c, output_dir, cp.name)
        c.Clear()

    for cp in combinedPlot2D.li_combined_plots2D: 

        c.SetRightMargin(0.16)


        ROOT.gStyle.SetPalette(55)  
        c.SetLogz()
        ROOT.gStyle.SetPaintTextFormat("4.2f")     
            
        # If not set, determine the y-range
        if cp.max_y == None:

            # Find the maximum y-value of the histgorams
            found_max = max([dic_histos2D[cp.name + "_" + p.name].GetMaximum() for p in cp.li_plots2D])

            # Set the y-range accordingly
            # extend furhter for logarithmic y-axes
            if cp.log_y:
                cp.max_y = 2*found_max
            else:
                cp.max_y = 1.25*found_max
                # End of cp.max_y == None

        # Loop over plots
        for i_p, p in enumerate(cp.li_plots2D):

            # Get the histogram
            h = dic_histos2D[cp.name + "_" + p.name]
            
            # Adjust y-range        
            """if cp.log_y:
                                                    h.SetAxisRange(0.1, cp.max_y,"y")
                                                    h.GetYaxis().SetLimits(0.01,cp.max_y)
                                                    c.SetLogy(True)
                                                else:
                                                    h.SetAxisRange(0.0001, cp.max_y,"y")
                                                    h.GetYaxis().SetLimits(0,cp.max_y)
                                                    c.SetLogy(False)"""
                # end of y-range adjusting

            # reduce number of ticks on x-axis
            h.GetXaxis().SetNdivisions(5,5,0)
            h.GetXaxis().SetRangeUser(cp.min_x,cp.max_x)
            h.GetYaxis().SetRangeUser(cp.min_y,cp.max_y)
            # Label the x-axis
            # proper adding of [units] to the x-axis label
            bin_width = h.GetBinWidth( 1 )
            if cp.axis_unit:
                h.GetXaxis().SetTitle( cp.label_x + " [" + cp.axis_unit + "]")
            else:
                h.GetXaxis().SetTitle( cp.label_x )

            # Label the y-axis
            #h.GetYaxis().SetTitle( cp.label_y + " / "+str(bin_width) +" "+ cp.axis_unit)
            h.GetYaxis().SetTitle( cp.label_y)
            h.GetYaxis().SetTitleOffset(1.5)
            h.GetXaxis().SetTitleOffset(1)


            if cp.normalize == True:
                scale = 1/h.GetMaximum()
                h.Scale(scale)

            print p.name, h.GetEntries()

            # Draw the histogram
            if i_p == 0:

                h.GetYaxis().SetNdivisions(505)
                h.GetXaxis().SetNdivisions(510)

                if cp.option == "text":
                    h.Draw("COLZ TEXT")
                else:
                    h.Draw("COLZ")


                xaxis = array( 'f' )
                yaxis = array( 'f' )
                xaxis.append(0.32)
                yaxis.append(0.6)
    
                hgra = ROOT.TGraph(1,xaxis,yaxis)
                hgra.SetMarkerColor(ROOT.kRed)
                hgra.SetMarkerStyle(29)
                hgra.SetMarkerSize(5)
    
                hgra.Draw("P")
    

                txt = ROOT.TText()
                txt.SetTextFont(61)
                txt.SetTextSize(0.05)
                txt.DrawTextNDC(0.16, 0.94, "CMS")
#
                txt.SetTextFont(52)
                txt.SetTextSize(0.04)
                txt.DrawTextNDC(0.28, 0.94, "Work In Progress")
#
                txt.SetTextFont(41)
                txt.DrawTextNDC(0.72, 0.94, "13 TeV")
            else:
                h.Draw("SAME")
        
        # Save the results to a file (in different formats)
        OutputDirectoryHelper.ManyPrint( c, output_dir, cp.name )
     
    # end of loop over combinedPlots
# end of drawHistograms


########################################
# doWork
########################################

def doWork(dic_files, output_dir):
   """ doWork: Inclusive function (histogram making+drawing) for local use"""

   # First create the histograms
   dic_histos, dic_histos2D = createHistograms(dic_files)

   # And draw them
   drawHistograms(dic_histos, dic_histos2D, output_dir)

# end of doWork
