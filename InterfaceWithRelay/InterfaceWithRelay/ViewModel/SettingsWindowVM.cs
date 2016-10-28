using InterfaceWithRelay.Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace InterfaceWithRelay.ViewModel
{
    public class SettingsWindowVM: IViewModel
    {
        private Window window;

        internal SettingsModel settingsModel = new SettingsModel();

        public SettingsWindowVM(Window win)
        {
            this.window = win;
        }
    }
}
