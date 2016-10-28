using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InterfaceWithRelay.Model
{
    public class CourseFolderInfo
    {
        public string CourseName { get; set; }
        public string FolderPath { get; set; }
        public List<FileInfo> fileList = new List<FileInfo>();

        public void UpdateLocalFileList()
        {

        }
    }
}
