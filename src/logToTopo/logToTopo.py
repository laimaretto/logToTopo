
import ipaddress
import sys
import argparse

## installed
import pandas as pd
import networkx as nx
from pyvis.network import Network
import numpy as np

D_TRUE_FALSE = {
    'no':False,
    'yes':True,
}

MY_OPRTIONS = """
    const options = {
    "nodes": {
        "borderWidth": null,
        "borderWidthSelected": null,
        "opacity": 0.7,
        "font": {
        "size": 14
        },
        "size": null
    },
    "edges": {
        "color": {
        "inherit": true
        },
        "font": {
        "size": 10,
        "align": "middle"
        },
        "selfReferenceSize": null,
        "selfReference": {
        "angle": 0.7853981633974483
        },
        "smooth": {
        "forceDirection": "none"
        }
    },
    "physics": {
        "minVelocity": 0.5
    }
    }
    """

def addNodes(dfSystem, G, size=5):

    for node in dfSystem.itertuples():

        system = node.INTERFACE_IP.replace('/32','')
        name   = node.NAME
        
        G.add_node(
                    name,
                    label = name+"\n"+system, 
                    system =system, 
                    size  =size
                    )

    return G

def addEdges(dfEdges, G, weight=1):
    """
    Generate Edges from a table with point-to-point interfaces
    The relationship between p2p is generated by the /30 o /31 subnet

    Args:
        dfEdges (_type_): _description_
        G (_type_): _description_
        weight (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """

    if isinstance(G, nx.Graph):
        nodeList = list(G.nodes)
    else:
        nodeList = [x['id'] for x in G.nodes]

    for edge in dfEdges.itertuples():

        name_0 = edge.NAME_0
        name_1 = edge.NAME_1
        port_0 = edge.INTERFACE_PORT_0
        port_1 = edge.INTERFACE_PORT_1
        network = edge.network
        label   = f'{port_0}--{port_1}' 

        if name_0 not in nodeList:
            # We dont have name_0, probably an unknown end, We add it as general sink
            G.add_node(name_0, label='na', system='na', size=3, color='red')
        elif name_1 not in nodeList:
            # We dont have name_1, probably an unknown end, We add it as general sink
            G.add_node(name_1, label='na', system='na', size=3, color='red')
        else:
            pass

        G.add_edge(name_0,name_1, port_0=port_0, port_1=port_1, network=network, weight=weight, label=label)



    return G

def getDf(xlsFile, sheetName='sh_rtr_iface'):

    df = pd.read_excel(xlsFile, sheet_name=sheetName)

    dfSystem = df[df.INTERFACE_NAME=='system']
    dfSystem = dfSystem[['NAME','INTERFACE_IP']]

    df1 = df.drop(columns='Index')
    df1 = df1.dropna(axis=0, how='all')
    df1 = df1.dropna(axis=1, how='all')
    df1['network'] = df1['INTERFACE_IP'].apply(lambda x: ipaddress.IPv4Interface(x).network).astype(str)
    df1 = df1[['network','INTERFACE_PORT','NAME']]

    dfEdges = (df1.assign(count=df1.groupby(['network']).cumcount()).pivot(index='network', columns='count'))
    dfEdges.columns = ["_".join(str(x) for x in i) for i in dfEdges.columns]
    dfEdges = dfEdges.reset_index()
    dfEdges = dfEdges[~dfEdges.network.str.contains('/32')]
    dfEdges = dfEdges.replace(np.nan,'na')

    return dfSystem, dfEdges

def main():

    parser1 = argparse.ArgumentParser(description='Topology Frapher', prog='PROG', usage='%(prog)s [options]')
    parser1.add_argument('-v'  ,'--version',     help='Version', action='version', version='Lucas Aimaretto - (c)2022 - laimaretto@gmail.com - Version: 1.0.0' )

    parser1.add_argument('-xf'  ,'--xlsFile', type=str, required=True, help='Name of Excel file where information about interfaces and subnets, reside.')
    parser1.add_argument('-xs'  ,'--xlsSheetName', type=str, default='sh_rtr_iface', help='Name of excel sheet, where data resides.')

    parser1.add_argument('-sm'  ,'--selectMenu', type=str, default='no', choices=['no','yes'], help='Show select menu in the topology.')
    parser1.add_argument('-fm'  ,'--filterMenu', type=str, default='no', choices=['no','yes'], help='Show filter menu in the topology.')

    args = parser1.parse_args()

    xlsFile       = args.xlsFile
    xlsSheetName  = args.xlsSheetName
    filterMenu    = D_TRUE_FALSE[args.filterMenu]
    selectMenu    = D_TRUE_FALSE[args.selectMenu]

    dfSystem, dfEdges = getDf(xlsFile, xlsSheetName)

    G  = nx.Graph()
    G  = addNodes(dfSystem,G)
    G  = addEdges(dfEdges, G)

    nt = Network(filter_menu=filterMenu, select_menu=selectMenu)
    nt.set_options(MY_OPRTIONS)
    nt.from_nx(G)
    nt.show('nx.html')

if __name__ == '__main__':

    main()