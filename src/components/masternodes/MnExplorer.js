import React, { useEffect, useState, useRef, useMemo } from 'react';
import { get } from 'utils/requests';
import Navbar from 'components/navbar/Navbar';
import TableDash from 'components/tables/TableDash';

export function MasternodesExplorer() {
    const columns = useMemo(
        () => [
          {
            Header: "Rank",
            accessor: "rank",
          },
          {
            Header: "Address",
            accessor: "addr",
          },
          {
            Header: "IP",
            accessor: "ip",
          },
          {
            Header: "Status",
            accessor: "status",
          },
          {
            Header: "Last Paid",
            accessor: "lastpaid",
          },
        ],
        []
      );
    
      const [getMns, setGetMns] = useState([]);
      useMemo(() => get(
        'api/mnlist',
        (response) => setGetMns(response),
        (error) => console.error(error)
      ), []);


    return (
        <div className='container'>
          <Navbar />
          <div className='box'>
          <TableDash columns={columns} data={getMns} />
          </div>
        </div>
 );
}
export default MasternodesExplorer;