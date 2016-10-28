using InterfaceWithRelay.ViewModel;
using MahApps.Metro.Controls;
using System.Windows;

namespace InterfaceWithRelay
{
    /// <summary>
    /// AppWindow.xaml 的交互逻辑
    /// </summary>
    public partial class AppWindow : MetroWindow
    {
        public AppWindow()
        {
            InitializeComponent();
            this.DataContext = new AppWindowVM(this);
        }
    }
}
