using InterfaceWithRelay.ViewModel;
using MahApps.Metro.Controls;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace InterfaceWithRelay
{
    /// <summary>
    /// SettingsWindow.xaml 的交互逻辑
    /// </summary>
    public partial class SettingsWindow : MetroWindow
    {
        public SettingsWindow(AppWindowVM appVM)
        {
            InitializeComponent();
            this.DataContext = new SettingsWindowVM(this);
        }

        public SettingsWindowVM ObtainViewModel()
        {
            return (this.DataContext as SettingsWindowVM);
        }
    }
}
