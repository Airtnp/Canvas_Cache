﻿using System;
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
using System.Windows.Navigation;
using System.Windows.Shapes;
using InterfaceWithRelay.ViewModel;

namespace InterfaceWithRelay
{
    /// <summary>
    /// LoginPage.xaml 的交互逻辑
    /// </summary>
    public partial class LoginPage : Page
    {
        public LoginPage()
        {
            InitializeComponent();
            this.DataContext = new LoginWindowVM(this);
        }

        private void passwordBox_LostFocus(object sender, RoutedEventArgs e)
        {
            // This was done in order to ensure the security of password.
            (DataContext as LoginWindowVM).LoginPassword = passwordBox.Password;
        }
    }
}
