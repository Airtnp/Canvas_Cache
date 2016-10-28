using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InterfaceWithRelay.Model
{
    public struct FileInfo
    {
        string fileName;
        DateTime lastUpdatedTime;
        int size;
        string path;
    }
}
