using System;
using System.IO;

namespace InterfaceWithRelay.Model
{
    public class CanvasFileInfo
    {
        private FileInfo fileInfo;

        public string Name
        {
            get { return fileInfo.Name; }
        }
        public DateTime LastAccessTime
        {
            get { return fileInfo.LastAccessTime; }
            set { fileInfo.LastAccessTime = value; }
        }
        public long Length
        {
            get { return fileInfo.Length; }
        }
        public string FullName
        {
            get { return fileInfo.FullName; }
        }

        private bool isLocal;
        public bool IsLocal
        {
            get { return isLocal; }
            set { isLocal = value; }
        }

        public CanvasFileInfo(string path, bool isLocal)
        {
            fileInfo = new FileInfo(path);
            this.isLocal = isLocal;
        }
    }
}
